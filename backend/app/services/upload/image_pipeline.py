import os
import hashlib

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

from app.services.image_embedding_service import (
    embed_image
)

from app.services.image_context_service import (
    get_page_text
)


# ---------------------------------------------------------
# Duplicate Removal
# ---------------------------------------------------------

def remove_duplicate_images(images):

    unique = []

    hashes = set()

    for image in images:

        try:

            with open(image["path"], "rb") as f:

                h = hashlib.md5(f.read()).hexdigest()

            if h in hashes:

                os.remove(image["path"])

                continue

            hashes.add(h)

            unique.append(image)

        except Exception:

            unique.append(image)

    return unique


# ---------------------------------------------------------
# Image Processing Pipeline
# ---------------------------------------------------------

def process_images(
    file_path,
    document_id,
    pages,
    source_file
):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    page_lookup = {

        page["page_no"]: page["text"]

        for page in pages

    }

    # -----------------------------------------------------
    # Extract Images
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # Remove duplicates
    # -----------------------------------------------------

    images = remove_duplicate_images(images)

    print()

    print("Unique Images :", len(images))

    print()

    # -----------------------------------------------------
    # Understand every image
    # -----------------------------------------------------

    processed = []

    for image in images:

        if not os.path.exists(image["path"]):

            continue

        understanding = understand_image(

            image["path"]

        )

        image["caption"] = understanding["caption"]

        image["ocr_text"] = understanding["ocr_text"]

        try:

            image["vision"] = analyze_image(

                image["path"]

            )

        except Exception:

            image["vision"] = ""

        image["page_text"] = get_page_text(

            page_lookup,

            image["page_no"]

        )

        image["source_file"] = source_file

        image["file_type"] = os.path.splitext(

            source_file

        )[1].lower()

        image["document_id"] = document_id

        # -----------------------------------------
        # CLIP Embedding
        # -----------------------------------------

        try:

            image["clip_embedding"] = embed_image(

                image["path"]

            )

        except Exception:

            image["clip_embedding"] = None

        processed.append(image)

    return processed