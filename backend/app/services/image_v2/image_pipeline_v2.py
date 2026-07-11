import os

from app.services.image_v2.extractor import ImageExtractor

from .metadata_analyzer import analyze_metadata
from .quality_analyzer import analyze_quality
from .ocr_metadata import compute_ocr_metadata
from .layout_metadata import analyze_layout

from .duplicate_detector import (
    detect_exact_duplicates,
    detect_similar_duplicates
)

from .florence.florence_loader import load_florence
from .florence.florence_caption import generate_captions
from .florence.semantic_decision import semantic_decision
from .florence.context_analyzer import analyze_context

from .decision_initializer import initialize_decision


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

    ####################################################
    # Stage 1 : Extraction
    ####################################################

    print("\n==============================")
    print("STAGE 1 : IMAGE EXTRACTION")
    print("==============================")

    extractor = ImageExtractor(document_id)

    images = extractor.extract(file_path)

    print(f"Extracted : {len(images)}")

    ####################################################
    # Stage 1.2 : Metadata
    ####################################################

    print("\n==============================")
    print("STAGE 1.2 : IMAGE METADATA")
    print("==============================")

    images = analyze_metadata(
        images,
        page_lookup
    )

    print(f"Metadata : {len(images)}")

    ####################################################
    # Stage 2 : Quality
    ####################################################

    print("\n==============================")
    print("STAGE 2 : IMAGE QUALITY")
    print("==============================")

    images = analyze_quality(images)

    print(f"Quality : {len(images)}")

    ####################################################
    # Stage 3 : OCR Metadata
    ####################################################

    print("\n==============================")
    print("STAGE 3 : OCR METADATA")
    print("==============================")

    images = compute_ocr_metadata(images)

    print(f"OCR Metadata : {len(images)}")

    ####################################################
    # Stage 4 : Layout
    ####################################################

    print("\n==============================")
    print("STAGE 4 : LAYOUT ANALYZER")
    print("==============================")

    images = analyze_layout(images)

    print(f"Layout : {len(images)}")

    ####################################################
    # Stage 5.1 : Exact Duplicate
    ####################################################

    print("\n==============================")
    print("STAGE 5.1 : EXACT DUPLICATE")
    print("==============================")

    images = detect_exact_duplicates(images)

    print(f"Remaining : {len(images)}")

    ####################################################
    # Stage 5.2 : Similar Duplicate
    ####################################################

    print("\n==============================")
    print("STAGE 5.2 : SIMILAR DUPLICATE")
    print("==============================")

    images = detect_similar_duplicates(images)

    print(f"Remaining : {len(images)}")

    ####################################################
    # Stage 6.1 : Load Florence
    ####################################################

    print("\n==============================")
    print("STAGE 6.1 : LOAD FLORENCE")
    print("==============================")

    processor, model = load_florence()

    ####################################################
    # Stage 6.2 : Caption Generation
    ####################################################

    print("\n==============================")
    print("STAGE 6.2 : GENERATE CAPTIONS")
    print("==============================")

    images = generate_captions(
        images,
        processor,
        model
    )

    print(f"Captioned : {len(images)}")

    ####################################################
    # Caption Sample
    ####################################################

    print("\n==============================")
    print("CAPTION SAMPLE")
    print("==============================")

    for image in images[:3]:

        print(f"\nPage {image.page_no}")
        print(image.path)
        print(image.florence_caption)

    ####################################################
    # Stage 6.5 : Semantic Decision
    ####################################################

    print("\n==============================")
    print("STAGE 6.5 : SEMANTIC DECISION")
    print("==============================")

    images = semantic_decision(images)

    print(f"Semantic Decision : {len(images)}")

    ####################################################
    # Stage 6.6 : Context Analyzer
    ####################################################

    print("\n==============================")
    print("STAGE 6.6 : CONTEXT ANALYZER")
    print("==============================")

    images = analyze_context(images)

    print(f"Context : {len(images)}")

    ####################################################
    # Stage 7.1 : Decision Initializer
    ####################################################

    print("\n==============================")
    print("STAGE 7.1 : DECISION INITIALIZER")
    print("==============================")

    images = initialize_decision(images)

    print(f"Initialized : {len(images)}")

    ####################################################
    # Pipeline Complete (Current Stage)
    ####################################################

    print("\n==============================")
    print("IMAGE PIPELINE COMPLETE")
    print("==============================")

    return images