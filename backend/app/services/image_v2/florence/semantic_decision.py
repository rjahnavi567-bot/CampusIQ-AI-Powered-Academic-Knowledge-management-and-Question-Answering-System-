# --------------------------------------------------
# Stage 6.5
# Semantic Decision
# --------------------------------------------------

KEEP_KEYWORDS = [

    "diagram",
    "architecture",
    "workflow",
    "flowchart",
    "pipeline",
    "algorithm",

    "graph",
    "chart",
    "plot",
    "histogram",

    "table",

    "equation",
    "formula",

    "scientific",
    "chemical",
    "medical",
    "microscope",

    "machine",
    "equipment",

    "illustration",

    "educational",

    "network",

    "system",

    "block diagram",

    "labeled"

]

REMOVE_KEYWORDS = [

    "paragraph",

    "text only",

    "page of text",

    "document page",

    "heading",

    "title",

    "logo",

    "icon",

    "watermark",

    "blank",

    "decorative",

    "toolbar",

    "menu",

    "user interface",

    "software screenshot",

    "application window"

]


def decide_image(image):

    text = (
        image.florence_caption
        + " "
        + image.reason
    ).lower()

    keep = 0
    remove = 0

    for word in KEEP_KEYWORDS:

        if word in text:

            keep += 1

    for word in REMOVE_KEYWORDS:

        if word in text:

            remove += 1

    image.keep_votes = keep
    image.remove_votes = remove

    if keep > remove:

        image.semantic_decision = "KEEP"

    elif remove > keep:

        image.semantic_decision = "REMOVE"

    else:

        image.semantic_decision = "UNKNOWN"

    return image


def semantic_decision(images):

    print("\n==============================")
    print("SEMANTIC DECISION")
    print("==============================")

    keep = 0
    remove = 0
    unknown = 0

    for image in images:

        decide_image(image)

        if image.semantic_decision == "KEEP":
            keep += 1

        elif image.semantic_decision == "REMOVE":
            remove += 1

        else:
            unknown += 1

    print(f"Images : {len(images)}")
    print(f"KEEP    : {keep}")
    print(f"REMOVE  : {remove}")
    print(f"UNKNOWN : {unknown}")

    print("\nSample\n")

    for image in images[:5]:

        print(f"Page : {image.page_no}")
        print("Caption :", image.florence_caption)
        print("Reason  :", image.reason)
        print("Decision:", image.semantic_decision)
        print("KeepVotes:", image.keep_votes)
        print("RemoveVotes:", image.remove_votes)
        print()

    return images