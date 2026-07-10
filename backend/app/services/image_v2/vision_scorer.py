# --------------------------------------------------
# Vision Scorer
# --------------------------------------------------

GOOD_CLASSES = [

    "diagram",

    "flowchart",

    "graph",

    "chart",

    "table",

    "equation",

    "photo"

]


BAD_CLASSES = [

    "paragraph",

    "text_page",

    "logo",

    "icon",

    "handwritten",

    "screenshot"

]


# --------------------------------------------------
# Compute Vision Score
# --------------------------------------------------

def compute_vision_score(image):

    positive = [

        image.diagram_score,

        image.flowchart_score,

        image.graph_score,

        image.chart_score,

        image.table_score,

        image.equation_score,

        image.photo_score

    ]

    negative = [

        image.paragraph_score,

        image.text_page_score,

        image.logo_score,

        image.icon_score,

        image.handwritten_score,

        image.screenshot_score

    ]

    ####################################################
    # Best useful prediction
    ####################################################

    useful = max(positive)

    ####################################################
    # Best useless prediction
    ####################################################

    useless = max(negative)

    score = useful - 0.25 * useless

    score = max(score, 0)
    score = min(score, 1)

    image.vision_score = round(score, 3)

    return image


# --------------------------------------------------
# Batch
# --------------------------------------------------

def score_vision(images):

    print("\n==============================")

    print("VISION SCORER")

    print("==============================")

    for image in images:

        compute_vision_score(image)

    print(f"Vision scored : {len(images)}")

    print("\nSample Scores")

    for image in images[:5]:

        print(

            f"Page {image.page_no} | "

            f"Vision Score = {image.vision_score:.3f}"

        )

    return images