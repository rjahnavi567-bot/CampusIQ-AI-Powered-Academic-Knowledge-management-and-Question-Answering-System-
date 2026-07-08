# --------------------------------------------------
# Final Decision Threshold
# --------------------------------------------------

USEFUL_SCORE_THRESHOLD = 0.70


# --------------------------------------------------
# Decide One Image
# --------------------------------------------------

def decide_image(image):

    ##################################################
    # Hard rejection always wins
    ##################################################

    if image.hard_reject:

        image.keep_image = False

        if image.decision_reason == "":
            image.decision_reason = "Hard Rule"

        image.decision_log.append("Rejected by Hard Rule")

        return image

    ##################################################
    # Useful Score
    ##################################################

    if image.useful_score >= USEFUL_SCORE_THRESHOLD:

        image.keep_image = True

        image.decision_reason = (
            f"Useful Score ({image.useful_score:.3f})"
        )

        image.decision_log.append(
            "Accepted by Useful Score"
        )

    else:

        image.keep_image = False

        image.decision_reason = (
            f"Low Useful Score ({image.useful_score:.3f})"
        )

        image.decision_log.append(
            "Rejected by Useful Score"
        )

    return image


# --------------------------------------------------
# Batch
# --------------------------------------------------

def decide_images(images):

    print("\n==============================")
    print("FINAL DECISION ENGINE")
    print("==============================")

    kept = 0
    removed = 0

    for image in images:

        decide_image(image)

        if image.keep_image:
            kept += 1
        else:
            removed += 1

    print(f"Images processed : {len(images)}")
    print(f"Keep            : {kept}")
    print(f"Remove          : {removed}")

    print("\nSample Decisions")

    for image in images[:5]:

        print(

            f"Page {image.page_no} | "

            f"Keep={image.keep_image} | "

            f"Score={image.useful_score:.3f} | "

            f"{image.decision_reason}"

        )

    return images