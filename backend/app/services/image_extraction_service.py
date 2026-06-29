import fitz
import os
from PIL import Image
import cv2
def is_meaningful_image(image_path):

    try:

        img = Image.open(image_path)

        width, height = img.size

        # Skip tiny images

        if width < 200 or height < 200:

            return False

        area = width * height

        # Skip icons/logos

        if area < 50000:

            return False

        return True

    except:

        return False

def is_full_page_scan(image_path):

    try:

        img = cv2.imread(image_path)

        h, w = img.shape[:2]

        ratio = w / h

        # Typical PDF page shape

        if 0.65 <= ratio <= 0.85:

            area = w * h

            if area > 1000000:

                return True

        return False

    except:

        return False

def extract_pdf_images(
    pdf_path,
    document_id
):

    images = []

    pdf = fitz.open(pdf_path)

    folder = (
        f"uploads/images/{document_id}"
    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    for page_no in range(
        len(pdf)
    ):

        page = pdf[page_no]

        for index, img in enumerate(
            page.get_images(
                full=True
            )
        ):

            xref = img[0]

            base = pdf.extract_image(xref)

            width = base.get("width", 0)
            height = base.get("height", 0)
            page_rect = page.rect

            page_width = page_rect.width
            page_height = page_rect.height

            if (
    width > page_width * 0.9 and
    height > page_height * 0.9
):
                continue

            if width < 150 or height < 150:
                     continue

            image_bytes = (
                base["image"]
            )

            ext = (
                base["ext"]
            )

            path = (
                f"{folder}/pdf_"
                f"{page_no}_{index}.{ext}"
            )

            with open(
                path,
                "wb"
            ) as f:

                f.write(
                    image_bytes
                )

            if (
    is_meaningful_image(path)
    and
    not is_full_page_scan(path)
):

                images.append({

        "path": path,

        "page_no": page_no + 1
    })

            else:

               os.remove(path)

    return images

import zipfile

def extract_docx_images(
    docx_path,
    document_id
):

    images = []

    folder = (
        f"uploads/images/{document_id}"
    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    with zipfile.ZipFile(
        docx_path,
        "r"
    ) as docx:

        for file in docx.namelist():

            if (
                "word/media/"
                in file
            ):

                filename = (
                    os.path.basename(
                        file
                    )
                )

                path = (
                    f"{folder}/{filename}"
                )

                with open(
                    path,
                    "wb"
                ) as f:

                    f.write(
                        docx.read(
                            file
                        )
                    )

                if (
    is_meaningful_image(path)
    and
    not is_full_page_scan(path)
):

                    images.append({

        "path": path,

        "page_no": 1
    })

                else:

                    os.remove(path)

    return images

from pptx import Presentation

def extract_pptx_images(
    pptx_path,
    document_id
):

    images = []

    folder = (
        f"uploads/images/{document_id}"
    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    prs = Presentation(
        pptx_path
    )

    for slide_index, slide in enumerate(
        prs.slides
    ):

        for shape in slide.shapes:

            if hasattr(
                shape,
                "image"
            ):

                image = (
                    shape.image
                )

                path = (
                    f"{folder}/slide_"
                    f"{slide_index}.png"
                )
                print(path)
                with open(
                    path,
                    "wb"
                ) as f:

                    f.write(
                        image.blob
                    )

                if (
    is_meaningful_image(path)
    and
    not is_full_page_scan(path)
):

                    images.append({

        "path": path,

        "page_no": slide_index + 1
    })

                else:

                    os.remove(path)

    return images


def extract_image_file(
    image_path
):

    return [
        {
            "path": image_path,
            "page_no": 1
        }
    ]

def extract_images(
    file_path,
    document_id
):

    extension = (
        os.path.splitext(file_path)[1]
        .lower()
    )

    if extension == ".pdf":

        return extract_pdf_images(
            file_path,
            document_id
        )

    elif extension == ".docx":

        return extract_docx_images(
            file_path,
            document_id
        )

    elif extension == ".pptx":

        return extract_pptx_images(
            file_path,
            document_id
        )

    elif extension in [
        ".jpg",
        ".jpeg",
        ".png"
    ]:

        return extract_image_file(
            file_path
        )

    return []