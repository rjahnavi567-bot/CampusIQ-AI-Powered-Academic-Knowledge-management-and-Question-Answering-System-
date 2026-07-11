# --------------------------------------------------
# Stage 7.1
# Decision Initializer
# --------------------------------------------------

def initialize_image(image):

    # Decision
    image.keep_image = True

    image.hard_reject = False

    image.decision_reason = ""

    image.decision_log = []

    # Individual Scores
    image.metadata_score = 0.0
    image.quality_score = 0.0
    image.ocr_score = 0.0
    image.layout_score = 0.0
    image.vision_score = 0.0
    image.duplicate_score = 0.0

    # Final Score
    image.useful_score = 0.0

    return image


# --------------------------------------------------
# Stage 7.1
# Decision Initializer
# --------------------------------------------------

def initialize_decision(images):

    print("\n==============================")
    print("DECISION INITIALIZER")
    print("==============================")

    for image in images:

        image.keep_image = True

        image.hard_reject = False

        image.decision_reason = ""

        image.decision_log = []

        image.useful_score = 0

        image.metadata_score = 0

        image.quality_score = 0

        image.ocr_score = 0

        image.layout_score = 0

        image.vision_score = 0

        image.duplicate_score = 0

    print(f"Initialized : {len(images)}")

    return images