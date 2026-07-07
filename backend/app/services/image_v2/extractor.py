import os
import fitz

from .page_renderer import render_page
from .layout_detector import detect_figures
from .region_detector import detect_regions
from .region_fusion import fuse_regions
from .crop_service import crop_regions
from .validator.validator import PipelineValidator

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
            # Stage 2 : PPStructure Layout Detection
            ####################################################

            layout_regions = detect_figures(page_image)

            print(
                f"PPStructure Regions : {len(layout_regions)}"
            )

            ####################################################
            # Stage 3 : Region Detection
            ####################################################

            region_boxes = detect_regions(page_image)

            print(
                f"OpenCV Regions      : {len(region_boxes)}"
            )

            ####################################################
            # Stage 4 : Region Fusion
            ####################################################

            detections = fuse_regions(
                layout_regions,
                region_boxes
            )

            print(
                f"Final Regions       : {len(detections)}"
            )
            ####################################################
# Stage 5.5 : Pipeline Validator
####################################################

            self.validator.validate(

    page_no=page_index + 1,

    page_image=page_image,

    layout_boxes=layout_regions,

    region_boxes=region_boxes,

    fusion_boxes=detections

)

            ####################################################
            # Stage 5 : Crop Extraction
            ####################################################

            page_candidates = crop_regions(

                page_image=page_image,

                page_no=page_index + 1,

                detections=detections,

                output_dir=self.output_dir,

                document_id=self.document_id

            )

            print(
                f"Crops Saved         : {len(page_candidates)}"
            )

            candidates.extend(page_candidates)

        pdf.close()

        print("\n========================================")
        print(f"TOTAL IMAGES EXTRACTED : {len(candidates)}")
        print("========================================\n")

        return candidates