from .score_calculator import calculate_final_score


HIGH_THRESHOLD = 0.75
LOW_THRESHOLD = 0.45


def decide(image):

    calculate_final_score(image)

    if image.hard_reject:

        image.keep_image = False
        image.confidence = 1.0
        image.final_decision = "REJECT"

        return image

    if image.final_score >= HIGH_THRESHOLD:

        image.keep_image = True
        image.final_decision = "KEEP"

    elif image.final_score < LOW_THRESHOLD:

        image.keep_image = False
        image.final_decision = "REJECT"

    else:

        image.keep_image = True
        image.final_decision = "REVIEW"

    image.confidence = round(

        abs(image.final_score - 0.5) * 2,

        3

    )

    return image


def decide_images(images):

    print("\n==============================")
    print("STAGE 8 : DECISION ENGINE")
    print("==============================")

    keep = 0
    reject = 0
    review = 0

    for image in images:

        decide(image)

        if image.final_decision == "KEEP":
            keep += 1

        elif image.final_decision == "REJECT":
            reject += 1

        else:
            review += 1

    print(f"KEEP   : {keep}")
    print(f"REJECT : {reject}")
    print(f"REVIEW : {review}")

    print("\nSample Decisions\n")

    for image in images[:10]:

        print(

            f"Page {image.page_no:3} | "

            f"Score={image.final_score:.3f} | "

            f"{image.final_decision:7} | "

            f"Confidence={image.confidence:.2f}"

        )

    return images