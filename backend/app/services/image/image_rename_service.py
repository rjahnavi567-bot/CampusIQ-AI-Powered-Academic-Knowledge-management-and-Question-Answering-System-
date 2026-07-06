import os

from app.services.image.image_filter_service import (
    clean_filename,
    generate_image_hash
)


def rename_image(image, document_id):
    """
    Rename image using:

    documentId_title_page_hash.ext

    Example

    15_cpu_architecture_page32_ab12cd34.png
    """

    image_hash = generate_image_hash(
        image["path"]
    )

    image["image_hash"] = image_hash

    safe_title = clean_filename(

        image.get(
            "title",
            "diagram"
        )

    )

    extension = os.path.splitext(
        image["path"]
    )[1]

    folder = os.path.dirname(
        image["path"]
    )

    base = (

        f"{document_id}_"

        f"{safe_title}"

        f"_page{image['page_no']}"

        f"_{image_hash}"

    )

    new_path = os.path.join(

        folder,

        base + extension

    )

    counter = 1
    if image["path"] == new_path:
        return image

    while os.path.exists(new_path):

        new_path = os.path.join(

            folder,

            f"{base}_{counter}{extension}"

        )

        counter += 1

    try:

        if image["path"] != new_path:

            os.rename(

                image["path"],

                new_path

            )

            image["path"] = new_path

    except Exception as e:

        print(

            "Rename Error:",

            e

        )

    return image