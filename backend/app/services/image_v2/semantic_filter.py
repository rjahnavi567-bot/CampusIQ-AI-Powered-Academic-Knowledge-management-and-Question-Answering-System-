REMOVE_CATEGORIES = {

    "logo",
    "icon",
    "paragraph",
    "text page",
    "page background",
    "watermark",
    "blank page"

}


MIN_CONFIDENCE = 0.45


def filter_semantic(images):

    print("\n========== SEMANTIC FILTER ==========")

    kept = []
    removed = 0

    for image in images:

        category = image.category.lower()

        confidence = image.classification_confidence

        if (
            category in REMOVE_CATEGORIES
            and confidence >= MIN_CONFIDENCE
        ):

            removed += 1
            continue

        kept.append(image)

    print(f"Input    : {len(images)}")
    print(f"Kept     : {len(kept)}")
    print(f"Removed  : {removed}")
    print("====================================\n")

    return kept