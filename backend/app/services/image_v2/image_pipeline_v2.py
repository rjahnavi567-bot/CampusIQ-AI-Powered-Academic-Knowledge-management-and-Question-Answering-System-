import os

from app.services.image_v2.extractor import ImageExtractor

from app.services.image_v2.duplicate_filter import remove_duplicates

from app.services.image_v2.caption_service import caption_images
from app.services.image_v2.image_classifier_service import classify_images
from app.services.image_v2.ocr_service import run_ocr
from app.services.image_v2.classifier import classify_image
from app.services.image_v2.quality_filter import (keep_image, filter_images)
from app.services.image_v2.metadata_builder import build_all_metadata
from app.services.image_v2.embedding_pipeline import generate_embeddings
def process_images_v2(
        file_path,
        document_id,
        page_lookup
):

    extension = os.path.splitext(

        file_path

    )[1].lower()

    if extension != ".pdf":

        raise Exception(

            "Stage-1 currently supports PDF only."

        )

    extractor = ImageExtractor(

        document_id

    )
    images = extractor.extract(file_path)
    print(f"Extracted : {len(images)}")

    images = remove_duplicates(images)
    print(f"After duplicate removal : {len(images)}")
    images = filter_images(images)

    print("Quality filter:", len(images))
    images = classify_images(images)

    print("Classification completed.")
    for img in images:

        print(
        img.path,
        img.width,
        img.height
    )
    images = caption_images(images)
    print("Caption completed.")

    images = run_ocr(images)
    print("OCR completed.")
    images = build_all_metadata(
    images,
    page_lookup
)
    print("Metadata completed.")
    images = generate_embeddings(images)
    print("Embedding completed.")
    print("\nPipeline Complete")

    return images
