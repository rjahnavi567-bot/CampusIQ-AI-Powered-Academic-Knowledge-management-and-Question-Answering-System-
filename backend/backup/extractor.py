import os
import numpy as np
import cv2
from PIL import Image
from .layout_detector import detect_figures
from .region_detector import detect_regions
from .region_fusion import fuse_regions
from .crop_service import crop_regions
from .sliding_window_detector import detect_window_figures
from .visual_object_detector import detect_visual_objects
from .visual_object_filter import filter_visual_objects
from .visual_object_merger import merge_visual_objects
from app.services.image_v2.improve.region_refiner import refine_regions
from .final_detection_fusion import final_fusion
from app.services.page_sources.batch_loader import load_document_batches
from .crop_service import crop_regions
from .improve.nms import non_max_suppression
from .improve.containment_filter import remove_contained_boxes
from .validator.validator import PipelineValidator
from .sliding_window_detector import generate_windows
from .sliding_window_detector import detect_window_figures
from .sliding_window_fusion import merge_window_detections
from .improve.figure_grouper import group_figures
from app.services.image_v2.improve.text_filter.text_heavy_filter import (
    filter_text_heavy
)
from app.services.statistics import collector
from app.services.statistics.timer import Timer
from itertools import islice
from concurrent.futures import ThreadPoolExecutor, as_completed
class ImageExtractor:

  def __init__(self, document_id):

        self.document_id = document_id

        self.output_dir = f"uploads/images/{document_id}"
        

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )
        self.validator = PipelineValidator(
    self.output_dir
)
    
  def process_page(self, page):

        page_no = page["page_no"]
        page_image = page["image"]

        if isinstance(page_image, Image.Image):

            page_image = cv2.cvtColor(
            np.array(page_image),
            cv2.COLOR_RGB2BGR
        )

        print("\n========================================")
        print(f"Processing Page {page_no}")
        print("========================================")

    ####################################################
    # Stage 2 : PPStructure
    ####################################################

        layout_regions = detect_figures(page_image)

    ####################################################
    # Stage 3 : Region Detector
    ####################################################

        region_boxes = detect_regions(page_image)

    ####################################################
    # Stage 4 : Region Fusion
    ####################################################

        regions = fuse_regions(
        layout_regions,
        region_boxes
    )

    ####################################################
    # Stage 5 : Sliding Window
    ####################################################

        window_detections = detect_window_figures(page_image)

    ####################################################
    # Stage 5.6 : Visual Objects
    ####################################################

        visual_objects = detect_visual_objects(page_image)

        visual_objects = filter_visual_objects(
        page_image,
        visual_objects
    )

        visual_objects = merge_visual_objects(
        visual_objects
    )

    ####################################################
    # Final Fusion
    ####################################################

        all_detections = final_fusion(
        regions,
        window_detections,
        visual_objects
    )

        all_detections = refine_regions(
        all_detections,
        page_image
    )

        all_detections = non_max_suppression(
        all_detections
    )

        all_detections = remove_contained_boxes(
        all_detections
    )

        all_detections = group_figures(
        all_detections,
        page_image
    )

        before_filter = len(all_detections)

        filter_timer = Timer()
        filter_timer.start()

        all_detections = filter_text_heavy(
        page_image,
        all_detections
    )

        filter_time = filter_timer.stop()

    ####################################################
    # Crop
    ####################################################

        page_candidates = crop_regions(
        page_image=page_image,
        page_no=page_no,
        detections=all_detections,
        output_dir=self.output_dir,
        document_id=self.document_id
    )

        return {

        "candidates": page_candidates,

        "layout": len(layout_regions),

        "regions": len(region_boxes),

        "windows": len(window_detections),

        "visual": len(visual_objects),

        "final": len(all_detections),

        "rejected": before_filter - len(all_detections),

        "filter_time": filter_time
    }

    ############################################################
  def create_batches(self, pages, batch_size):

    pages = iter(pages)

    while True:

        batch = list(islice(pages, batch_size))

        if not batch:
            break

        yield batch

  def extract(self, file_path):

    image_timer = Timer()
    image_timer.start()

    candidates = []

    page_batches = load_document_batches(
    file_path,
    batch_size=4
)

    total_layout = 0
    total_regions = 0
    total_windows = 0
    total_visual = 0
    total_final = 0
    total_text_rejected = 0

    # -----------------------------
    # MULTITHREADED PAGE PROCESSING
    # -----------------------------

    max_workers = 4

    batch_size = 4

    for batch_no, batch in enumerate(
    page_batches,
    start=1
):

        print("\n==============================")
        print(f"BATCH {batch_no}")
        print("==============================")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:

            futures = {
            executor.submit(
                self.process_page,
                page
            ): page["page_no"]
            for page in batch
        }

            for future in as_completed(futures):

                result = future.result()

                candidates.extend(result["candidates"])

                collector.add_time(
                "Image Filtering Time",
                result["filter_time"]
            )

                collector.increment(
                "Total Useful Images Retained",
                result["final"]
            )

                collector.increment(
                "Total Useless Images Filtered",
                result["rejected"]
            )

                collector.increment(
                "Total Images Extracted",
                len(result["candidates"])
            )

                collector.increment(
                "Total Images Classified",
                len(result["candidates"])
            )

                total_layout += result["layout"]
                total_regions += result["regions"]
                total_windows += result["windows"]
                total_visual += result["visual"]
                total_final += result["final"]
                total_text_rejected += result["rejected"]

    print(f"PPStructure : {total_layout}")
    print(f"Region Detector : {total_regions}")
    print(f"Sliding Window : {total_windows}")
    print(f"Visual Objects : {total_visual}")
    print(f"Final Detections : {total_final}")
    print(f"Text Heavy Rejected : {total_text_rejected}")

    print("\n========================================")
    print(f"TOTAL IMAGES EXTRACTED : {len(candidates)}")
    print("========================================\n")

    image_time = image_timer.stop()

    collector.add_time(
        "Image Extraction Time",
        image_time
    )

    return candidates