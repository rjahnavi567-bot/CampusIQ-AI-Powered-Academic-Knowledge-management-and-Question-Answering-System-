# --------------------------------------------------
# Layout Scorer
# --------------------------------------------------

GOOD_COMPONENTS = 50
GOOD_CONTOURS = 30
GOOD_LINES = 10


# --------------------------------------------------
# Layout Type Score
# --------------------------------------------------

def score_layout_type(image):

    scores = {

        "diagram": 1.0,

        "chart": 0.95,

        "table": 0.90,

        "photo": 0.85,

        "unknown": 0.50

    }

    return scores.get(

        image.layout_type,

        0.50

    )


# --------------------------------------------------
# Connected Components
# --------------------------------------------------

def score_components(image):

    if image.connected_components >= GOOD_COMPONENTS:

        return 1.0

    return image.connected_components / GOOD_COMPONENTS


# --------------------------------------------------
# Contour Score
# --------------------------------------------------

def score_contours(image):

    if image.contour_count >= GOOD_CONTOURS:

        return 1.0

    return image.contour_count / GOOD_CONTOURS


# --------------------------------------------------
# Line Score
# --------------------------------------------------

def score_lines(image):

    total = (

        image.horizontal_lines +

        image.vertical_lines

    )

    if total >= GOOD_LINES:

        return 1.0

    return total / GOOD_LINES




# --------------------------------------------------
# Final Layout Score
# --------------------------------------------------

def compute_layout_score(image):
    if image.hard_reject:

        image.layout_score = 0.0

        return image

    layout = score_layout_type(image)

    components = score_components(image)

    contours = score_contours(image)

    lines = score_lines(image)

    image.layout_score = round(

    (

        layout +

        components +

        contours +

        lines

    ) / 4,

    3

)

    return image


# --------------------------------------------------
# Batch
# --------------------------------------------------

def score_layout(images):

    print("\n==============================")

    print("LAYOUT SCORER")

    print("==============================")

    for image in images:

        compute_layout_score(image)

    print(f"Layout scored : {len(images)}")

    print("\nSample Scores")

    for image in images[:5]:

        print(

            f"Page {image.page_no} | "

            f"{image.layout_type:8} | "

            f"Layout Score = {image.layout_score:.3f}"

        )

    return images