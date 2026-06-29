import os

from app.services.image_extraction_service import (
    extract_pdf_images,
    extract_docx_images,
    extract_pptx_images,
    extract_image_file,
    extract_images
)

from app.services.image_understanding_service import (
    understand_image
)

from app.services.groq_vision_service import (
    analyze_image
)

from app.services.clip_service import (
    create_image_embedding
)

from app.services.image_context_service import (
    get_page_text
)


def process_images(
    file_path,
    document_id,
    pages
):
    """
    Complete image processing pipeline.

    Returns:
        images
    """

    extension = os.path.splitext(
        file_path
    )[1].lower()

    page_lookup = {}

    for page in pages:

        page_lookup[
            page["page_no"]
        ] = page["text"]

    # -------------------------
    # Extract Images
    # -------------------------

    if extension == ".pdf":

        images = extract_pdf_images(
            file_path,
            document_id
        )

    elif extension == ".docx":

        images = extract_docx_images(
            file_path,
            document_id
        )

    elif extension == ".pptx":

        images = extract_pptx_images(
            file_path,
            document_id
        )

    elif extension in [
        ".png",
        ".jpg",
        ".jpeg"
    ]:

        images = extract_image_file(
            file_path
        )

    else:

        images = extract_images(
            file_path,
            document_id
        )

    # -------------------------
    # Understand Images
    # -------------------------

    for image in images:

        understanding = understand_image(
            image["path"]
        )

        image["caption"] = understanding["caption"]

        image["ocr_text"] = understanding["ocr_text"]

        # ---------------------
        # Groq Vision
        # ---------------------

        try:

            image["vision"] = analyze_image(
                image["path"]
            )

        except Exception as e:

            print(
                "Groq Vision Error:",
                e
            )

            image["vision"] = ""

        # ---------------------
        # Page Context
        # ---------------------

        image["page_text"] = get_page_text(

            page_lookup,

            image["page_no"]

        )

        # ---------------------
        # CLIP Embedding
        # ---------------------

        try:

            image["clip_embedding"] = (
                create_image_embedding(
                    image["path"]
                )
            )

        except Exception as e:

            print(
                "CLIP Error:",
                e
            )

            image["clip_embedding"] = None

    return images