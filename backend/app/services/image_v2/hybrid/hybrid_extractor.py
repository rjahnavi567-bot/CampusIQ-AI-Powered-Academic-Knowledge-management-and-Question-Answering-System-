import os
import cv2
import fitz  # PyMuPDF
import numpy as np
from PIL import Image
from doclayout_yolo import YOLO

from app.services.image_v2.doclayout.region_extractor import extract_regions
from .hybrid_visualizer import draw_boxes
from .compare_results import compare_results
from .hybrid_merger import merge_boxes
class HybridExtractor:
  def process_document(self, pdf_path):

    pages = self.pdf_to_pages(pdf_path)

    all_regions = []

    for page in pages:

        print(f"\nProcessing Page {page['page_no']}")

        image = page["image"]

        results = self.model.predict(

            source=image,

            conf=0.25,

            verbose=False

        )

        output_folder = os.path.join(

            "doclayout_regions",

            f"page_{page['page_no']}"

        )

        regions = extract_regions(

            results,

            output_folder

        )

        draw_boxes(

            image=image,

            boxes=regions,

            save_path=f"doclayout_visual_page_{page['page_no']}.jpg"

        )

        all_regions.append({

            "page_no": page["page_no"],

            "regions": regions

        })

    return all_regions
  def pdf_to_pages(self, pdf_path):

    doc = fitz.open(pdf_path)

    pages = []

    for page_no in range(len(doc)):

        page = doc.load_page(page_no)

        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        img = cv2.cvtColor(
            np.array(img),
            cv2.COLOR_RGB2BGR
        )

        pages.append({

            "page_no": page_no + 1,

            "image": img

        })

    return pages

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
        # Fake old detections for now
        old_regions = []

        compare_results(
    old_regions,
    regions
)

        # Draw detections
        draw_boxes(
            image=image,
            boxes=regions,
            save_path="hybrid_result.jpg"
        )

        return regions