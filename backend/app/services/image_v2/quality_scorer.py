# --------------------------------------------------
# Quality Scorer
# --------------------------------------------------

GOOD_BLUR = 150.0
MIN_BLUR = 20.0

GOOD_NOISE = 15.0
MAX_NOISE = 60.0

GOOD_EDGE = 0.05
MIN_EDGE = 0.003


# --------------------------------------------------
# Blur Score
# --------------------------------------------------

def score_blur(image):

    if image.blur_score >= GOOD_BLUR:
        return 1.0

    if image.blur_score <= MIN_BLUR:
        return 0.0

    return (
        image.blur_score - MIN_BLUR
    ) / (
        GOOD_BLUR - MIN_BLUR
    )


# --------------------------------------------------
# Noise Score
# --------------------------------------------------

def score_noise(image):

    if image.noise_score <= GOOD_NOISE:
        return 1.0

    if image.noise_score >= MAX_NOISE:
        return 0.0

    return 1 - (

        (image.noise_score - GOOD_NOISE)

        /

        (MAX_NOISE - GOOD_NOISE)

    )


# --------------------------------------------------
# Edge Density Score
# --------------------------------------------------

def score_edges(image):

    if image.edge_density >= GOOD_EDGE:
        return 1.0

    if image.edge_density <= MIN_EDGE:
        return 0.0

    return (

        image.edge_density - MIN_EDGE

    ) / (

        GOOD_EDGE - MIN_EDGE

    )


# --------------------------------------------------
# Empty Image Score
# --------------------------------------------------

def score_empty(image):

    return 0.0 if image.is_empty else 1.0


# --------------------------------------------------
# Background Score
# --------------------------------------------------

def score_background(image):

    return 0.0 if image.background_only else 1.0


# --------------------------------------------------
# Compute Final Quality Score
# --------------------------------------------------

def compute_quality_score(image):
    if image.hard_reject:

        image.quality_score = 0.0

        return image

    blur = score_blur(image)

    noise = score_noise(image)

    edge = score_edges(image)

    empty = score_empty(image)

    background = score_background(image)

    image.quality_score = round(

        (

            blur +
            noise +
            edge +
            empty +
            background

        ) / 5,

        3

    )

    return image


# --------------------------------------------------
# Batch Scoring
# --------------------------------------------------

def score_quality(images):

    print("\n==============================")
    print("QUALITY SCORER")
    print("==============================")

    for image in images:

        compute_quality_score(image)

    print(f"Quality scored : {len(images)}")

    print("\nSample Scores")

    for image in images[:5]:

        print(

            f"Page {image.page_no} | "

            f"Quality Score = {image.quality_score:.3f}"

        )

    return images