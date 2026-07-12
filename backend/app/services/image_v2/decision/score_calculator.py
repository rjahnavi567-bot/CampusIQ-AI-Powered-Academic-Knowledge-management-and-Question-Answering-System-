from .weights import *


def calculate_final_score(image):

    score = (

        image.metadata_score * METADATA_WEIGHT +

        image.quality_score * QUALITY_WEIGHT +

        image.ocr_score * OCR_WEIGHT +

        image.layout_score * LAYOUT_WEIGHT +

        image.vision_score * VISION_WEIGHT

    )

    image.final_score = round(score, 3)

    return image