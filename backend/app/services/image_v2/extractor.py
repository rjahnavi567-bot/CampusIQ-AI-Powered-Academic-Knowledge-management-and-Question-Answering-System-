import os
import fitz
import cv2
import numpy as np

from PIL import Image

from .models import ImageCandidate


class ImageExtractor:

    def __init__(self, document_id):

        self.document_id = document_id

        self.output = f"uploads/images/{document_id}"

        os.makedirs(self.output, exist_ok=True)

    #############################################################

    def extract(self, pdf_path):

        pdf = fitz.open(pdf_path)

        images = []

        for page_no in range(len(pdf)):

            page = pdf.load_page(page_no)

            images.extend(

                self.extract_embedded_images(

                    pdf,
                    page,
                    page_no
                )

            )

            images.extend(

                self.extract_vector_figures(

                    page,
                    page_no
                )

            )

        return images

    #############################################################

    def extract_embedded_images(

            self,
            pdf,
            page,
            page_no
    ):

        candidates = []

        images = page.get_images(full=True)

        seen = set()

        for img in images:

            xref = img[0]

            if xref in seen:
                continue

            seen.add(xref)

            try:

                base = pdf.extract_image(xref)

            except:

                continue

            ext = base["ext"]

            data = base["image"]

            filename = os.path.join(

                self.output,

                f"embedded_{page_no}_{xref}.{ext}"

            )

            with open(filename, "wb") as f:

                f.write(data)

            image = cv2.imread(filename)

            if image is None:

                os.remove(filename)

                continue

            h, w = image.shape[:2]

            candidates.append(

                ImageCandidate(

                    path=filename,

                    page_no=page_no + 1,

                    source="embedded",

                    bbox=None,

                    width=w,

                    height=h,

                    area=w*h,

                    document_id=self.document_id,

                    image_type="embedded"

                )

            )

        return candidates

    #############################################################

    def extract_vector_figures(

            self,
            page,
            page_no
    ):

        drawings = page.get_drawings()

        if not drawings:

            return []

        pix = page.get_pixmap(

            matrix=fitz.Matrix(3,3)

        )

        page_image = os.path.join(

            self.output,

            f"page_{page_no}.png"

        )

        pix.save(page_image)

        image = cv2.imread(page_image)

        if image is None:

            return []

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

            (5,5)

        )

        binary = cv2.dilate(

            binary,

            kernel,

            iterations=2

        )

        contours,_ = cv2.findContours(

            binary,

            cv2.RETR_EXTERNAL,

            cv2.CHAIN_APPROX_SIMPLE

        )

        candidates=[]

        idx=0

        page_area=image.shape[0]*image.shape[1]

        for c in contours:

            x,y,w,h=cv2.boundingRect(c)

            area=w*h

            if area<40000:
                continue

            if area>page_area*0.85:
                continue

            crop=image[y:y+h,x:x+w]

            save=os.path.join(

                self.output,

                f"vector_{page_no}_{idx}.png"

            )

            cv2.imwrite(save,crop)

            idx+=1

            candidates.append(

                ImageCandidate(

                    path=save,

                    page_no=page_no+1,

                    source="vector",

                    bbox=(x,y,w,h),

                    width=w,

                    height=h,

                    area=area,

                    document_id=self.document_id,

                    image_type="vector"

                )

            )

        try:

            os.remove(page_image)

        except:

            pass

        return candidates