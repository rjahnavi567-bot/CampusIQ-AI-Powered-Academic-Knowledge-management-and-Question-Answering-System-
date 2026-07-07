import os
import fitz

from .page_renderer import render_page
from .layout_detector import detect_figures
from .region_detector import detect_regions
from .region_fusion import fuse_regions
from .crop_service import crop_regions
from .sliding_window_detector import detect_window_figures
from .visual_object_detector import detect_visual_objects
from .visual_object_filter import filter_visual_objects
from .visual_object_merger import merge_visual_objects

from .final_detection_fusion import final_fusion

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

    def extract(self, pdf_path):

        pdf = fitz.open(pdf_path)

        candidates = []

        for page_index in range(len(pdf)):

            print("\n========================================")
            print(f"Processing Page {page_index + 1}")
            print("========================================")

            ####################################################
            # Stage 1 : Render Page
            ####################################################

            page = pdf.load_page(page_index)

            page_image = render_page(page)

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

    page_no=page_index + 1,

    detections=all_detections,

    output_dir=self.output_dir,

    document_id=self.document_id

)

            candidates.extend(page_candidates)
        print(f"PPStructure: {len(layout_regions)}")
        print(f"Region Detector: {len(region_boxes)}")
        print(f"Sliding Window: {len(window_detections)}")
        print(f"Visual Objects: {len(visual_objects)}")
        print(f"Final Detections: {len(all_detections)}")
        pdf.close()

        print("\n========================================")
        print(f"TOTAL IMAGES EXTRACTED : {len(candidates)}")
        print("========================================\n")

        return candidates