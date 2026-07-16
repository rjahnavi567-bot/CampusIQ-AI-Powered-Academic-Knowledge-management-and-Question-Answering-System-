import cv2

from .crop_saver import save_crop
from .models import ImageCandidate
from app.services.image_v2.improve.page_classifier import classify_full_page
from .improve.adaptive_expander import adaptive_expand
from app.services.image_v2.improve.border_trimmer import trim_white_border
# ----------------------------------------
# Minimum crop size
# ----------------------------------------

MIN_WIDTH = 40
MIN_HEIGHT = 40


def crop_regions(

    page_image,
    page_no,
    detections,
    output_dir,
    document_id

):

    """
    Crop every detected region.

    Returns:
        list[ImageCandidate]
    """

    page_height, page_width = page_image.shape[:2]

    candidates = []

    index = 0

    for det in detections:

        x1, y1, x2, y2 = adaptive_expand(
    det["bbox"],
    page_image.shape
)

        ###################################################
        # Keep crop inside page
        ###################################################

        x1 = max(0, x1)
        y1 = max(0, y1)

        x2 = min(page_width, x2)
        y2 = min(page_height, y2)

        ###################################################
        # Invalid box
        ###################################################

        if x2 <= x1:
            continue

        if y2 <= y1:
            continue

        ###################################################
        # Crop
        ###################################################

        crop = page_image[

            y1:y2,

            x1:x2

        ]
        if classify_full_page(crop, page_image.shape):

            print("Rejected full-page document")

            continue
        crop = trim_white_border(crop)

        if crop.size == 0:
            continue

        ###################################################
        # Ignore extremely tiny crops
        ###################################################

        h, w = crop.shape[:2]

        if w < MIN_WIDTH:
            continue

        if h < MIN_HEIGHT:
            continue

        ###################################################
        # Save crop
        ###################################################

        filename = save_crop(

            crop=crop,

            output_dir=output_dir,

            page_no=page_no,

            index=index

        )

        if filename is None:
            continue

        ###################################################
        # Create candidate
        ###################################################

        candidate = ImageCandidate(

            path=filename,

            page_no=page_no,

            width=w,

            height=h,

            area=w * h,

            bbox=(x1, y1, x2, y2),

            source=det.get(
                "source",
                "layout"
            ),

            category=det.get(
                "category",
                "figure"
            ),

            confidence_score=det.get(
                "confidence",
                1.0
            ),

            image_type="crop",

            document_id=document_id

        )

        candidates.append(candidate)

        index += 1

    print(f"Crops generated : {len(candidates)}")

    return candidates