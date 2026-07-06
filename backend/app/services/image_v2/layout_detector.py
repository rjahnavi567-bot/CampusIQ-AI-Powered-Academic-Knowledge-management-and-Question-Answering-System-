import os

import fitz

import cv2

import numpy as np

from paddleocr import PPStructure


layout_engine = PPStructure(
    show_log=False,
    layout=True,
    table=False,
    ocr=False
)


def detect_figures(pdf_path, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)

    figures = []

    for page_index in range(len(doc)):

        page = doc.load_page(page_index)

        pix = page.get_pixmap(
            matrix=fitz.Matrix(2,2)
        )

        image = np.frombuffer(
            pix.samples,
            dtype=np.uint8
        ).reshape(
            pix.height,
            pix.width,
            pix.n
        )

        if pix.n == 4:

            image = cv2.cvtColor(
                image,
                cv2.COLOR_RGBA2RGB
            )

        result = layout_engine(image)

        figure_no = 0

        for item in result:

            if item["type"] != "figure":
                continue

            x1,y1,x2,y2 = map(int,item["bbox"])

            crop = image[y1:y2,x1:x2]

            if crop.size == 0:
                continue

            filename = os.path.join(

                output_folder,

                f"page_{page_index+1}_figure_{figure_no}.png"

            )

            cv2.imwrite(filename,crop)

            figures.append({

                "page_no":page_index+1,

                "path":filename,

                "bbox":[x1,y1,x2,y2]

            })

            figure_no +=1

    return figures