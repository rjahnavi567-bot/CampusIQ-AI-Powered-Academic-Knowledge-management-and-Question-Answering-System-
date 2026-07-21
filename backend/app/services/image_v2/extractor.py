import os
import numpy as np
import cv2
from PIL import Image
from .crop_service import crop_regions
from app.services.image_v2.improve.region_refiner import refine_regions
from app.services.page_sources.batch_loader import load_document_batches
from .crop_service import crop_regions
from .improve.nms import non_max_suppression
from .improve.containment_filter import remove_contained_boxes
from .validator.validator import PipelineValidator
from .improve.figure_grouper import group_figures
from app.services.image_v2.improve.text_filter.text_heavy_filter import (
    filter_text_heavy
)
from .layout_detector import detect_figures_batch
from app.services.statistics import collector
from app.services.statistics.timer import Timer
from itertools import islice
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.services.image_v2.config import (
    USE_REGION_DETECTOR,
    USE_SLIDING_WINDOW,
    USE_VISUAL_OBJECTS
)
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
    
  def process_page_from_layout(self, page, detections):

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
# Stage 2 : DocLayout
####################################################

        all_detections = detections


####################################################
# Small refinement
####################################################

        all_detections = refine_regions(
    all_detections,
    page_image
)

####################################################
# NMS
####################################################

        all_detections = non_max_suppression(
    all_detections
)

####################################################
# Remove nested boxes
####################################################

        all_detections = remove_contained_boxes(
    all_detections
)

####################################################
# Group nearby figures
####################################################

        all_detections = group_figures(
    all_detections,
    page_image
)

####################################################
# Remove text-heavy crops
####################################################

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
    "layout": len(all_detections),

    "regions": 0,

    "windows": 0,

    "visual": 0,

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
    batch_size=8
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

    max_workers = 1

    batch_size = 4

    for batch_no, batch in enumerate(
    page_batches,
    start=1
):

        print("\n==============================")
        print(f"BATCH {batch_no}")
        print("==============================")

        # ------------------------------------------
# Convert pages to OpenCV images
# ------------------------------------------

        images = []

        for page in batch:

            page_image = page["image"]

            if isinstance(page_image, Image.Image):

                page_image = cv2.cvtColor(

            np.array(page_image),

            cv2.COLOR_RGB2BGR

        )

            images.append(page_image)

# ------------------------------------------
# ONE DocLayout inference for entire batch
# ------------------------------------------



        batch_layout = detect_figures_batch(images)

# ------------------------------------------
# Process each page using its detections
# ------------------------------------------

        for page, detections in zip(batch, batch_layout):

            result = self.process_page_from_layout(

        page,

        detections

    )

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

    print(f"DocLayout : {total_layout}")
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