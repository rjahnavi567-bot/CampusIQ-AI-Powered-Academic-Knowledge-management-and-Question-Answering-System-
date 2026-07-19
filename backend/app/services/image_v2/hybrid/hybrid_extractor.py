import os
import cv2

from doclayout_yolo import YOLO

from app.services.image_v2.doclayout.region_extractor import extract_regions
from .hybrid_visualizer import draw_boxes


class HybridExtractor:

    def __init__(self):

        self.model = YOLO(
            r"models/doclayout/doclayout_yolo_docstructbench_imgsz1024.pt"
        )

    def process_image(self, image_path):

        # Original image
        image = cv2.imread(image_path)

        # Run DocLayout
        results = self.model.predict(
            source=image_path,
            conf=0.25,
            verbose=False
        )

        output_folder = "doclayout_regions"

        regions = extract_regions(
            results,
            output_folder
        )

        # Draw detections
        draw_boxes(
            image=image,
            boxes=regions,
            save_path="hybrid_result.jpg"
        )

        return regions