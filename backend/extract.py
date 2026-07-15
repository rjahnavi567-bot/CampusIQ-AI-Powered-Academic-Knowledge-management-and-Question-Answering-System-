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

from .final_detection_fusion import final_fusion
from app.services.page_sources.source_loader import load_document
from .crop_service import crop_regions
from .validator.validator import PipelineValidator
from .sliding_window_detector import generate_windows
from .sliding_window_detector import detect_window_figures
from .sliding_window_fusion import merge_window_detections
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

    ############################################################

    def extract(self, file_path):

        candidates = []

        pages = load_document(file_path)
        total_layout = 0
        total_regions = 0
        total_windows = 0
        total_visual = 0
        total_final = 0

        for page in pages:

            page_no = page["page_no"]

            page_image = page["image"]
            # Convert PIL image to OpenCV image
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
# Stage 5 : Sliding Window Detector
####################################################

            window_detections = detect_window_figures(
    page_image
)

####################################################
# Stage 5.6 : Visual Object Detector
####################################################

            visual_objects = detect_visual_objects(
    page_image
)

####################################################
# Stage 5.6.2 : Visual Object Filter
####################################################

            visual_objects = filter_visual_objects(
    page_image,
    visual_objects
)

####################################################
# Stage 5.6.3 : Merge Visual Objects
####################################################

            visual_objects = merge_visual_objects(
    visual_objects
)

####################################################
# Stage 5.6.4 : Final Fusion
####################################################

            all_detections = final_fusion(
    regions,
    window_detections,
    visual_objects
)

####################################################
# Stage 6 : Crop Service
####################################################

            page_candidates = crop_regions(

    page_image=page_image,

    page_no=page_no,

    detections=all_detections,

    output_dir=self.output_dir,

    document_id=self.document_id

)
            

            candidates.extend(page_candidates)
            total_layout += len(layout_regions)
            total_regions += len(region_boxes)
            total_windows += len(window_detections)
            total_visual += len(visual_objects)
            total_final += len(all_detections)
        print(f"PPStructure : {total_layout}")
        print(f"Region Detector : {total_regions}")
        print(f"Sliding Window : {total_windows}")
        print(f"Visual Objects : {total_visual}")
        print(f"Final Detections : {total_final}")

        print("\n========================================")
        print(f"TOTAL IMAGES EXTRACTED : {len(candidates)}")
        print("========================================\n")

        return candidates