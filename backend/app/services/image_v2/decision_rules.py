# --------------------------------------------------
# Decision Rules
# --------------------------------------------------


USEFUL = {

    "diagram",
    "flowchart",
    "table",
    "graph",
    "chart",
    "equation"

}


BAD = {

    "paragraph",
    "heading",
    "logo",
    "icon",
    "watermark",
    "handwritten",
    "screenshot"

}


def apply_rules(image):

    categories = set(image.semantic_categories)

    # ----------------------------
    # Duplicate
    # ----------------------------

    if image.is_duplicate:

        image.keep_image = False
        return image

    # ----------------------------
    # Very Low Importance
    # ----------------------------

    if image.importance_score < 20:

        image.keep_image = False
        return image

    # ----------------------------
    # Bad Categories
    # ----------------------------

    if len(categories & BAD) > 0:

        if "diagram" not in categories:

            image.keep_image = False
            return image

    # ----------------------------
    # Useful Categories
    # ----------------------------

    if len(categories & USEFUL) > 0:

        if image.importance_score >= 40:

            image.keep_image = True

        else:

            image.keep_image = False

        return image

    # ----------------------------
    # Photo
    # ----------------------------

    if "photo" in categories:

        image.keep_image = image.importance_score >= 50

        return image

    # ----------------------------
    # Default
    # ----------------------------

    image.keep_image = image.importance_score >= 50

    return image


def apply_decision_rules(images):

    print("\n==============================")
    print("DECISION RULES")
    print("==============================")

    keep = 0
    remove = 0

    for image in images:

        apply_rules(image)

        if image.keep_image:

            keep += 1

        else:

            remove += 1

    print(f"Processed : {len(images)}")
    print(f"Keep      : {keep}")
    print(f"Remove    : {remove}")

    print("\nSample\n")

    for image in images[:10]:

        print(

            f"Page {image.page_no} | "

            f"Importance={image.importance_score} | "

            f"Keep={image.keep_image}"

        )

    return images