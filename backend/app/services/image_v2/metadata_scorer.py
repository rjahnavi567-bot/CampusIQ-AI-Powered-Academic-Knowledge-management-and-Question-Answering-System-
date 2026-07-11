# --------------------------------------------------
# Metadata Scorer
# --------------------------------------------------

MIN_RESOLUTION = 100 * 100          # 10,000 pixels
GOOD_RESOLUTION = 400 * 400         # 160,000 pixels

MIN_FILE_SIZE = 5 * 1024            # 5 KB
GOOD_FILE_SIZE = 100 * 1024         # 100 KB

GOOD_PAGE_RATIO = 0.05              # 5% of page


# --------------------------------------------------
# Resolution Score
# --------------------------------------------------

def score_resolution(image):

    pixels = image.width * image.height

    if pixels >= GOOD_RESOLUTION:
        return 1.0

    if pixels <= MIN_RESOLUTION:
        return 0.0

    return (
        pixels - MIN_RESOLUTION
    ) / (
        GOOD_RESOLUTION - MIN_RESOLUTION
    )


# --------------------------------------------------
# File Size Score
# --------------------------------------------------

def score_file_size(image):

    if image.file_size >= GOOD_FILE_SIZE:
        return 1.0

    if image.file_size <= MIN_FILE_SIZE:
        return 0.0

    return (
        image.file_size - MIN_FILE_SIZE
    ) / (
        GOOD_FILE_SIZE - MIN_FILE_SIZE
    )


# --------------------------------------------------
# Page Ratio Score
# --------------------------------------------------

def score_page_ratio(image):

    if image.page_ratio >= GOOD_PAGE_RATIO:
        return 1.0

    if image.page_ratio <= 0:
        return 0.0

    return image.page_ratio / GOOD_PAGE_RATIO


# --------------------------------------------------
# Aspect Ratio Score
# --------------------------------------------------

def score_aspect_ratio(image):

    ratio = image.aspect_ratio

    if 0.5 <= ratio <= 2.5:
        return 1.0

    if ratio < 0.2:
        return 0.0

    if ratio > 6.0:
        return 0.0

    if ratio < 0.5:
        return ratio / 0.5

    return max(
        0.0,
        1 - ((ratio - 2.5) / 3.5)
    )


# --------------------------------------------------
# Compute Metadata Score
# --------------------------------------------------

def compute_metadata_score(image):
    if image.hard_reject:

       image.metadata_score = 0.0

       return image
    

    resolution = score_resolution(image)

    file_size = score_file_size(image)

    page_ratio = score_page_ratio(image)

    aspect = score_aspect_ratio(image)

    image.metadata_score = round(

        (
            resolution +
            file_size +
            page_ratio +
            aspect
        ) / 4,

        3

    )

    return image


# --------------------------------------------------
# Batch
# --------------------------------------------------

def score_metadata(images):

    print("\n==============================")
    print("METADATA SCORER")
    print("==============================")

    for image in images:

        compute_metadata_score(image)

    print(f"Metadata scored : {len(images)}")

    print("\nSample Scores")

    for image in images[:5]:

        print(

            f"Page {image.page_no} | "

            f"Metadata Score = {image.metadata_score:.3f}"

        )

    return images