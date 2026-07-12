# ------------------------------------------
# Stage 6.3
# Early Reject Filter
# ------------------------------------------

MIN_PAGE_RATIO = 0.005
MIN_WIDTH = 40
MIN_HEIGHT = 40


def filter_images(images):

    print("\n==============================")
    print("STAGE 6.3 : EARLY FILTER")
    print("==============================")

    kept = []
    removed = 0

    for image in images:

        if image.is_duplicate:
            removed += 1
            continue

        if image.width < MIN_WIDTH:
            removed += 1
            continue

        if image.height < MIN_HEIGHT:
            removed += 1
            continue

        if image.page_ratio < MIN_PAGE_RATIO:
            removed += 1
            continue

        if image.is_empty:
            removed += 1
            continue

        if image.background_only:
            removed += 1
            continue

        kept.append(image)

    print(f"Input Images : {len(images)}")
    print(f"Kept         : {len(kept)}")
    print(f"Removed      : {removed}")

    return kept