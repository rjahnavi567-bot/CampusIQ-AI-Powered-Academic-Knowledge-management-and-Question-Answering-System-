# --------------------------------------------------
# Stage 9.5
# Search Text Builder
# --------------------------------------------------


def build_search_text(image):

    caption = getattr(
    image,
    "cleaned_caption",
    ""
)

    ocr = getattr(
    image,
    "cleaned_ocr",
    ""
)

    keywords = getattr(
        image,
        "keywords",
        []
    )

    metadata = getattr(
        image,
        "normalized_metadata",
        {}
    )

    layout = metadata.get(
        "layout",
        "unknown"
    )

    orientation = metadata.get(
        "orientation",
        "unknown"
    )

    resolution = metadata.get(
        "resolution",
        ""
    )

    keyword_text = " ".join(keywords)

    image.search_text = (

        f"Caption: {caption}\n"

        f"OCR: {ocr}\n"

        f"Keywords: {keyword_text}\n"

        f"Layout: {layout}\n"

        f"Orientation: {orientation}\n"

        f"Resolution: {resolution}"

    )

    return image


# --------------------------------------------------
# Batch
# --------------------------------------------------

def build_all_search_text(images):

    print("\n==============================")
    print("STAGE 9.5 : SEARCH TEXT")
    print("==============================")

    for image in images:

        build_search_text(image)

    print(f"Search Text Built : {len(images)}")

    print("\nSamples\n")

    for image in images[:3]:

        print(f"Page {image.page_no}")

        print(image.search_text)

        print("-" * 60)

    return images