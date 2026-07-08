# --------------------------------------------------
# Decision Initializer
# --------------------------------------------------

def initialize_decision(images):

    print("\n==============================")
    print("DECISION INITIALIZER")
    print("==============================")

    for image in images:

        ##################################################
        # Default values
        ##################################################

        image.keep_image = True

        image.useful_score = 0.0

        image.metadata_score = 0.0

        image.quality_score = 0.0

        image.ocr_score = 0.0

        image.layout_score = 0.0

        image.vision_score = 0.0

        image.duplicate_score = 0.0

        image.hard_reject = False

        image.decision_reason = ""

        image.decision_log = []

    print(f"Decision model initialized : {len(images)}")

    return images