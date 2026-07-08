import os

from app.services.image_v2.extractor import ImageExtractor
from .duplicate_detector import detect_exact_duplicates
from app.services.image_v2.basic_crop_validator import filter_figures
from app.services.image_v2.duplicate_filter import remove_duplicates
from app.services.image_v2.quality_filter import filter_images
from app.services.image_v2.layout_metadata import analyze_layout
from app.services.image_v2.image_classifier_service import classify_images
from .ocr_metadata import compute_ocr_metadata
from app.services.image_v2.caption_service import caption_images
from app.services.image_v2.ocr_service import run_ocr
from app.services.image_v2.quality_analyzer import analyze_quality
from app.services.image_v2.metadata_builder import build_all_metadata
from app.services.image_v2.embedding_pipeline import generate_embeddings
from app.services.image_v2.semantic_filter import filter_semantic
from app.services.image_v2.metadata_analyzer import analyze_metadata
def process_images_v2(
    file_path,
    document_id,
    page_lookup
):

    extension = os.path.splitext(file_path)[1].lower()

    if extension != ".pdf":
        raise Exception(
            "Stage-1 currently supports PDF only."
        )

    print("\n==============================")
    print("STAGE 1 : IMAGE EXTRACTION")
    print("==============================")

    extractor = ImageExtractor(document_id)
    images = extractor.extract(file_path)
    print("\After extract Filter")

    for img in images:
        print(img.path)


    print(f"Extracted : {len(images)}")
    print("\n==============================")
    print("STAGE 1 : IMAGE METADATA")
    print("==============================")

    images = analyze_metadata(
    images,
    page_lookup
)

    print(f"Metadata : {len(images)}")
    print("\n==============================")
    print("STAGE 2 : IMAGE QUALITY")
    print("==============================")

    images = analyze_quality(images)

    print(f"Quality : {len(images)}")
    print("\n==============================")
    print("STAGE 3 : OCR METADATA")
    print("==============================")

    images = compute_ocr_metadata(images)
    print(type(images))
    print(len(images))

    print(type(images[0]))


    print(f"OCR Metadata : {len(images)}")
    print("\n==============================")
    print("STAGE 4 : LAYOUT ANALYZER")
    print("==============================")

    images = analyze_layout(images)

    print(f"Layout : {len(images)}")
    ####################################################
# Stage 5 : Exact Duplicate Detector
####################################################

    print("\n==============================")
    print("STAGE 5 : EXACT DUPLICATE")
    print("==============================")

    images = detect_exact_duplicates(images)

    print(f"Remaining Images : {len(images)}")


    print("\n==============================")
    print("STAGE 2 : FIGURE FILTER")
    print("==============================")
    print("\nBefore Figure Filter")

    for img in images:
        print(img.path)

    images = filter_figures(images)

    print("\nAfter Figure Filter")

    for img in images:
        print(img.path)

    print(f"Remaining : {len(images)}")


    print("\n==============================")
    print("STAGE 3 : DUPLICATE REMOVAL")
    print("==============================")
    print("\nBEforeDuplicate Filter")

    for img in images:
        print(img.path)


    images = remove_duplicates(images)
    print("\After Duplicate Filter")

    for img in images:
        print(img.path)


    print(f"Remaining : {len(images)}")

    print("\n==============================")
    print("STAGE 5 : CLIP CLASSIFICATION")
    print("==============================")
    print("\Before Clip Filter")

    for img in images:
        print(img.path)


    images = classify_images(images)
    print("\After clip Filter")

    for img in images:
        print(img.path)


    print("\n==============================")
    print("STAGE 8 : SEMANTIC FILTER")
    print("==============================")

    images = filter_semantic(images)

    print(f"Remaining : {len(images)}")
    
    for image in images:

        print(
            f"Page {image.page_no:3} | "
            f"{image.category:25} | "
            f"{image.classification_confidence:.3f}"
        )

    print("\n==============================")
    print("STAGE 4 : QUALITY FILTER")
    print("==============================")
    print("\nBefore quality Filter")

    for img in images:
        print(img.path)


    images = filter_images(images)
    print("\After quality Filter")

    for img in images:
        print(img.path)


    print(f"Remaining : {len(images)}")



    print("\n==============================")
    print("STAGE 6 : IMAGE CAPTIONING")
    print("==============================")

    images = caption_images(images)

    print("Caption completed.")


    print("\n==============================")
    print("STAGE 7 : OCR")
    print("==============================")

    images = run_ocr(images)

    print("OCR completed.")


    print("\n==============================")
    print("STAGE 8 : METADATA")
    print("==============================")

    images = build_all_metadata(
        images,
        page_lookup
    )

    print("Metadata completed.")


    print("\n==============================")
    print("STAGE 9 : CLIP EMBEDDING")
    print("==============================")

    images = generate_embeddings(images)

    print("Embedding completed.")


    print("\n==============================")
    print("PIPELINE COMPLETE")
    print("==============================")

    return images