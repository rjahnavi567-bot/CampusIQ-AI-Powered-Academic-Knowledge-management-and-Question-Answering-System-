import os
import glob

from app.services.image_extraction_service import (
    extract_pdf_images,
    extract_docx_images,
    extract_pptx_images,
    extract_image_file,
    extract_images
)

from app.services.image.image_filter_service import (
    is_useful_image
)

from app.services.image.image_duplicate_service import (
    remove_duplicate_images,
    is_duplicate
)

from app.services.image.image_processor_service import (
    process_single_image
)

from app.services.image.image_embedding_batch_service import (
    generate_embeddings
)

from app.services.image.image_rename_service import (
    rename_image
)
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)
from app.services.image.academic_figure_detector import (
    is_academic_figure
)
def process_image_worker(
    image,
    page_lookup,
    source_file,
    document_id
):
    """
    Process one image.

    Runs inside a worker thread.
    """

    if not os.path.exists(image["path"]):
        return None

    if not is_useful_image(image["path"]):
        print(f"Rejected by useful filter: {os.path.basename(image['path'])}")
        try:
            os.remove(image["path"])
        except:
            pass

        return None

        # ------------------------------------------
# Academic Figure Filter
# ------------------------------------------
    
    if not is_academic_figure(image["path"]):

        print(
         "Rejected (Not Academic Figure):",
        os.path.basename(image["path"])
    )

        
        try:
            os.remove(image["path"])
        except:
            pass

        return None

    image = process_single_image(
        image,
        page_lookup
    )

    if image is None:
        print(f"Rejected by AI: {os.path.basename(image['path'])}")
        return None

    image["source_file"] = source_file

    image["file_type"] = os.path.splitext(
        source_file
    )[1].lower()

    image["document_id"] = document_id
    print(
    "Before rename:",
    os.path.basename(image["path"])
)

    image = rename_image(
        image,
        document_id
    )
    print(
    "After rename:",
    os.path.basename(image["path"])
)

    return image
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

    # ----------------------------------------
    # Image Extraction
    # ----------------------------------------

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

    # ----------------------------------------
    # Remove duplicate extracted images
    # ----------------------------------------
    images = remove_duplicate_images(
        images
    )
    print(f"After duplicate removal: {len(images)}")

    print()

    print(
        "Unique Images :",
        len(images)
    )

    print()
    processed = []
    print("\nProcessing images in parallel...\n")

    

    
    with ThreadPoolExecutor(
    max_workers = min(4, os.cpu_count() or 1)
) as executor:

        futures = [

        executor.submit(

            process_image_worker,

            image,

            page_lookup,

            source_file,

            document_id

        )

        for image in images

    ]
    print()

    for future in as_completed(futures):

        image = future.result()

        if image is None:
            continue

        if is_duplicate(
            processed,
            image
        ):

            try:
                print(
    "Duplicate removed:",
    os.path.basename(image["path"])
)
                os.remove(image["path"])
            except:
                pass

            continue

        processed.append(image)
        print(f"Accepted Images: {len(processed)}")
        print(
    f"Accepted: {os.path.basename(image['path'])}"
)
    print("\nImages after AI filtering:\n")

    for img in processed:

        print(os.path.basename(img["path"]))

    print(f"Count = {len(processed)}")
        

    # ----------------------------------------
    # Batch CLIP Embeddings
    # ----------------------------------------

    print()

    print(
        "Generating CLIP embeddings..."
    )

    processed = generate_embeddings(
        processed
    )

    print(

        f"Generated {len(processed)} embeddings."

    )

    # ----------------------------------------
    # Remove temporary page images
    # ----------------------------------------

    page_images = glob.glob(

        f"uploads/images/{document_id}/page_*.png"

    )

    for img in page_images:

        if os.path.exists(img):

            try:
                os.remove(img)
            except:
                pass

    print(f"Processing: {os.path.basename(image['path'])}")

    return processed