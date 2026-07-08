# --------------------------------------------------
# Duplicate Scorer
# --------------------------------------------------

def compute_duplicate_score(image):

    ##################################################
    # Exact / Similar duplicate
    ##################################################

    if image.is_duplicate:

        image.duplicate_score = 0.0

    else:

        image.duplicate_score = 1.0

    return image


# --------------------------------------------------
# Batch
# --------------------------------------------------

def score_duplicates(images):

    print("\n==============================")
    print("DUPLICATE SCORER")
    print("==============================")

    duplicates = 0

    for image in images:

        compute_duplicate_score(image)

        if image.is_duplicate:

            duplicates += 1

    print(f"Duplicate scored : {len(images)}")

    print(f"Duplicates : {duplicates}")

    print("\nSample Scores")

    for image in images[:5]:

        print(

            f"Page {image.page_no} | "

            f"Duplicate = {image.is_duplicate} | "

            f"Score = {image.duplicate_score:.3f}"

        )

    return images