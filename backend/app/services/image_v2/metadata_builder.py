import os


def build_metadata(image, page_context=""):

    image.page_text = page_context

    image.filename = os.path.basename(image.path)

    search_parts = [

        image.caption.strip(),

        image.ocr_text.strip(),

        page_context.strip()

    ]

    image.search_text = "\n".join(

    part

    for part in [

        image.caption,

        image.ocr_text,

        image.page_context,

        image.category

    ]

    if part

)

    return image


def build_all_metadata(images, page_lookup):

    print("\nBuilding metadata...")

    for image in images:

        page_context = page_lookup.get(
            image.page_no,
            ""
        )

        build_metadata(
            image,
            page_context
        )

    print("Metadata completed.")

    return images