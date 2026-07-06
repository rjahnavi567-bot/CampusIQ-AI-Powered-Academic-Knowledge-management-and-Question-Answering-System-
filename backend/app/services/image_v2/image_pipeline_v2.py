import os

from app.services.image_v2.extractor import ImageExtractor

from app.services.image_v2.duplicate_filter import remove_duplicates

from app.services.image_v2.caption_service import caption_images
from app.services.image_v2.image_classifier_service import classify_images
from app.services.image_v2.ocr_service import run_ocr
from app.services.image_v2.classifier import classify_image
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

    print(f"Candidates: {len(images)}")

    print("\nRunning Duplicate Removal...")
    images = remove_duplicates(images)

    print(f"Remaining Images : {len(images)}")
    images = caption_images(images)

    print("\nGenerating BLIP Captions...")
    images = caption_images(images)

    print("\nRunning OCR...")
    images = run_ocr(images)
    page_lookup = {}

    print("\nBuilding Metadata...")
    images = build_all_metadata(
    images,
    page_lookup
)

    print("\nGenerating CLIP Embeddings...")
    images = generate_embeddings(images)
    images = classify_image(images)
    images = classify_images(images)
    

    print("\nPipeline Complete")

    return images
