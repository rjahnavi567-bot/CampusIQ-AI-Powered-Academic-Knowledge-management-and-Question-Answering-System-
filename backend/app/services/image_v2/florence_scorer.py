# --------------------------------------------------
# Stage 7.7
# Florence Scorer
# --------------------------------------------------

POSITIVE = {

    "diagram":20,
    "architecture":20,
    "workflow":18,
    "flowchart":18,
    "pipeline":18,
    "algorithm":18,
    "network":15,
    "system":12,
    "component":12,
    "table":16,
    "graph":16,
    "chart":16,
    "plot":15,
    "equation":18,
    "formula":18,
    "matrix":15,
    "machine":12,
    "equipment":12,
    "laboratory":12,
    "microscope":15,
    "scientific":15,
    "chemical":15,
    "medical":15,
    "illustration":12

}

NEGATIVE = {

    "paragraph":-25,
    "page of text":-25,
    "text page":-25,
    "document page":-25,
    "heading":-18,
    "title":-12,
    "logo":-30,
    "icon":-20,
    "watermark":-40,
    "toolbar":-30,
    "desktop":-20,
    "window":-20,
    "software":-20,
    "menu":-20,
    "blank":-30

}


def compute_florence_score(image):

    if image.hard_reject:

        image.vision_score = 0.0

        return image

    caption = image.florence_caption.lower()

    score = 50

    for word, weight in POSITIVE.items():

        if word in caption:

            score += weight

    for word, weight in NEGATIVE.items():

        if word in caption:

            score += weight

    score = max(0, min(score, 100))

    image.vision_score = round(score / 100, 3)

    return image


def score_vision(images):

    print("\n==============================")
    print("FLORENCE SCORER")
    print("==============================")

    for image in images:

        compute_florence_score(image)

    print(f"Florence scored : {len(images)}")

    print("\nSample Scores\n")

    for image in images[:5]:

        print(f"Page {image.page_no}")

        print(image.florence_caption)

        print(f"Vision Score : {image.vision_score:.3f}")

        print()

    return images