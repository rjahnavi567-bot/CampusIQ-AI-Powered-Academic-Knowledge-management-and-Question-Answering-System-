# --------------------------------------------------
# Useful Score Calculator
# --------------------------------------------------

METADATA_WEIGHT = 0.10

QUALITY_WEIGHT = 0.15

OCR_WEIGHT = 0.20

LAYOUT_WEIGHT = 0.20

VISION_WEIGHT = 0.30

DUPLICATE_WEIGHT = 0.05


# --------------------------------------------------
# Compute Final Score
# --------------------------------------------------

def compute_useful_score(image):

    score = (

        image.metadata_score * METADATA_WEIGHT +

        image.quality_score * QUALITY_WEIGHT +

        image.ocr_score * OCR_WEIGHT +

        image.layout_score * LAYOUT_WEIGHT +

        image.vision_score * VISION_WEIGHT +

        image.duplicate_score * DUPLICATE_WEIGHT

    )

    image.useful_score = round(score, 3)

    return image


# --------------------------------------------------
# Batch
# --------------------------------------------------

def compute_useful_scores(images):

    print("\n==============================")
    print("USEFUL SCORE")
    print("==============================")

    for image in images:

        compute_useful_score(image)

    print(f"Useful scores computed : {len(images)}")

    print("\nSample Scores")

    for image in images[:5]:

        print(

            f"Page {image.page_no} | "

            f"Useful Score = {image.useful_score:.3f}"

        )

    return images