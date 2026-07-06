import os
import fitz
import cv2
import numpy as np

from .models import ImageCandidate


class ImageExtractor:

    def __init__(self, document_id):

        self.document_id = document_id

        self.output_dir = f"uploads/images/{document_id}"

        os.makedirs(self.output_dir, exist_ok=True)

    ###########################################################

    def extract(self, pdf_path):

        pdf = fitz.open(pdf_path)

        results = []

        for page_index in range(len(pdf)):

            page = pdf.load_page(page_index)

            results.extend(
                self.extract_embedded_images(
                    pdf,
                    page,
                    page_index
                )
            )

            results.extend(
                self.extract_vector_images(
                    page,
                    page_index
                )
            )

        pdf.close()

        print(f"\nTotal extracted : {len(results)}")

        return results
    
        ###########################################################

    def extract_embedded_images(
        self,
        pdf,
        page,
        page_index
    ):

        candidates = []

        seen = set()

        images = page.get_images(full=True)

        for image in images:

            xref = image[0]

            if xref in seen:
                continue

            seen.add(xref)

            try:

                base = pdf.extract_image(xref)

            except:

                continue

            ext = base["ext"]

            image_bytes = base["image"]

            filename = os.path.join(

                self.output_dir,

                f"embedded_{page_index}_{xref}.{ext}"

            )

            with open(filename, "wb") as f:

                f.write(image_bytes)

            img = cv2.imread(filename)

            if img is None:

                try:
                    os.remove(filename)
                except:
                    pass

                continue

            h, w = img.shape[:2]

            candidates.append(

                ImageCandidate(

                    path=filename,

                    page_no=page_index + 1,

                    width=w,

                    height=h,

                    area=w * h,

                    source="embedded",

                    image_type="embedded",

                    document_id=self.document_id

                )

            )

        return candidates
    
        ###########################################################

    def extract_vector_images(
        self,
        page,
        page_index
    ):

        candidates = []

        drawings = page.get_drawings()

        if not drawings:

            return candidates

        pix = page.get_pixmap(
            matrix=fitz.Matrix(3, 3)
        )

        page_image = os.path.join(

            self.output_dir,

            f"page_{page_index}.png"

        )

        pix.save(page_image)

        image = cv2.imread(page_image)

        if image is None:

            return candidates

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        binary = cv2.threshold(
            gray,
            240,
            255,
            cv2.THRESH_BINARY_INV
        )[1]

        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (5, 5)
        )

        binary = cv2.dilate(
            binary,
            kernel,
            iterations=2
        )

        contours, _ = cv2.findContours(
            binary,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        idx = 0

        page_area = image.shape[0] * image.shape[1]

        for contour in contours:

            x, y, w, h = cv2.boundingRect(contour)

            area = w * h

            if area < 10000:
                continue

            if area > page_area * 0.98:
                continue

            crop = image[y:y+h, x:x+w]

            filename = os.path.join(

                self.output_dir,

                f"vector_{page_index}_{idx}.png"

            )

            cv2.imwrite(filename, crop)

            idx += 1

            candidates.append(

                ImageCandidate(

                    path=filename,

                    page_no=page_index + 1,

                    width=w,

                    height=h,

                    area=area,

                    bbox=(x, y, w, h),

                    source="vector",

                    image_type="vector",

                    document_id=self.document_id

                )

            )

        try:
            os.remove(page_image)
        except:
            pass

        return candidates