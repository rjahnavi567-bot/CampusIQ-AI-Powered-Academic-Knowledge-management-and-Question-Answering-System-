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
from .hard_rules import apply_hard_rules

from .metadata_scorer import score_metadata
from .quality_scorer import score_quality
from .ocr_scorer import score_ocr
from .layout_scorer import score_layout
from .florence_scorer import score_vision
from .early_reject_filter import filter_images
from .decision.decision_engine import decide_images

from .stage9.caption_cleaner import clean_captions
from .stage9.ocr_cleaner import clean_ocrs
from .stage9.metadata_normalizer import normalize_all_metadata
from .stage9.keyword_extractor import extract_all_keywords
from .stage9.search_text_builder import build_all_search_text

from .embedding_generator import generate_embeddings
from .embedding_validator import validate_embeddings
from .vector_storage import store_vectors

from .vector_verifier import verify_vectors
from .context.context_pipeline import build_contexts
from app.services.page_sources.source_loader import load_document
from app.services.image_v2.improve.text_filter.edge_density_filter import filter_edge_density
from app.services.statistics import collector
from app.services.statistics.timer import Timer
from app.services.image_v2.layout_classifier.layout_service import (
    classify_images
)
from app.services.image_v2.figure_classifier.figure_service import (
    classify_figures
)
def process_images_v2(
    file_path,
    document_id,
    page_lookup,
    page_text_lookup
):
    

    ####################################################
# Stage 1 : Universal Document Loading
####################################################

    print("\n==============================")
    print("STAGE 1 : DOCUMENT LOADING")
    print("==============================")

    print(f"Input File : {os.path.basename(file_path)}")

####################################################
# Stage 1.1 : Image Extraction
####################################################

    print("\n==============================")
    print("STAGE 2 : IMAGE EXTRACTION")
    print("==============================")

    extractor = ImageExtractor(document_id)

    images = extractor.extract(file_path)

    print(f"Extracted Images : {len(images)}")
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
    # Stage 6.1 : Exact Duplicate
    ####################################################

    print("\n==============================")
    print("STAGE 6.1 : EXACT DUPLICATE")
    print("==============================")

    images = detect_exact_duplicates(images)

    print(f"Remaining : {len(images)}")

    ####################################################
    # Stage 6.2 : Similar Duplicate
    ####################################################

    print("\n==============================")
    print("STAGE 6.2 : SIMILAR DUPLICATE")
    print("==============================")

    images = detect_similar_duplicates(images)

    print(f"Remaining : {len(images)}")
    ####################################################
# Stage 6.3 : Early Reject
####################################################

    print("\n==============================")
    print("STAGE 6.3 : EARLY FILTER")
    print("==============================")

    images = filter_images(images)

    print(f"Remaining : {len(images)}")
    ####################################################
# Stage 6.3.1 : DocLayout Classification
####################################################

    print("\n==============================")
    print("STAGE 6.3.1 : DOCLAYOUT")
    print("==============================")

    images = classify_images(images)

    print(f"DocLayout : {len(images)}")
    ####################################################
# Stage 6.3.2 : SigLIP Figure Classification
####################################################

    print("\n==============================")
    print("STAGE 6.3.2 : SIGLIP")
    print("==============================")

    images = classify_figures(images)

    print(f"SigLIP : {len(images)}")

    ####################################################
    # Stage 6.4 : Load Florence
    ####################################################

    print("\n==============================")
    print("STAGE 6.4 : LOAD FLORENCE")
    print("==============================")

    processor, model = load_florence()

    ####################################################
    # Stage 6.5 : Caption Generation
    ####################################################

    print("\n==============================")
    print("STAGE 6.5 : GENERATE CAPTIONS")
    print("==============================")
    caption_timer = Timer()
    caption_timer.start()

    images = generate_captions(
        images,
        processor,
        model
    )

    caption_time = caption_timer.stop()
    caption_count = 0

    for img in images:

        if getattr(img, "caption", "").strip():

            caption_count += 1

    print(f"Captioned : {len(images)}")
    generated = sum(
    1
    for img in images
    if getattr(img, "caption", "").strip()
)

    collector.increment(
    "Total Image Captions Generated",
    generated
)

    collector.add_time(
    "Caption Generation Time",
    caption_time
)

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
    # Stage 6.6 : Semantic Decision
    ####################################################

    print("\n==============================")
    print("STAGE 6.6 : SEMANTIC DECISION")
    print("==============================")

    images = semantic_decision(images)

    print(f"Semantic Decision : {len(images)}")

    ####################################################
    # Stage 6.7 : Context Analyzer
    ####################################################

    print("\n==============================")
    print("STAGE 6.7 : CONTEXT ANALYZER")
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
# Stage 7.3 : Metadata Score
####################################################

    print("\n==============================")
    print("STAGE 7.3 : METADATA SCORE")
    print("==============================")

    images = score_metadata(images)

    print(f"Metadata Scored : {len(images)}")


####################################################
# Stage 7.4 : Quality Score
####################################################

    print("\n==============================")
    print("STAGE 7.4 : QUALITY SCORE")
    print("==============================")

    images = score_quality(images)

    print(f"Quality Scored : {len(images)}")


####################################################
# Stage 7.5 : OCR Score
####################################################

    print("\n==============================")
    print("STAGE 7.5 : OCR SCORE")
    print("==============================")

    images = score_ocr(images)

    print(f"OCR Scored : {len(images)}")


####################################################
# Stage 7.6 : Layout Score
####################################################

    print("\n==============================")
    print("STAGE 7.6 : LAYOUT SCORE")
    print("==============================")

    images = score_layout(images)

    print(f"Layout Scored : {len(images)}")


####################################################
# Stage 7.7 : Florence Score
####################################################

    print("\n==============================")
    print("STAGE 7.7 : FLORENCE SCORE")
    print("==============================")

    images = score_vision(images)

    print(f"Florence Scored : {len(images)}")
    ####################################################
# Stage 7.8 : Hard Rules
####################################################

    print("\n==============================")
    print("STAGE 7.8 : HARD RULES")
    print("==============================")

    images = apply_hard_rules(images)

    print(f"Hard Rules Completed : {len(images)}")


####################################################
# Stage 7 Summary
####################################################

    print("\n==============================")
    print("STAGE 7 SUMMARY")
    print("==============================")

    for image in images[:10]:

        print(
        f"Page {image.page_no:3} | "
        f"Metadata={image.metadata_score:.2f} | "
        f"Quality={image.quality_score:.2f} | "
        f"OCR={image.ocr_score:.2f} | "
        f"Layout={image.layout_score:.2f} | "
        f"Vision={image.vision_score:.2f} | "
        f"HardReject={image.hard_reject}"
    )
    ####################################################
# Stage 8 : Decision Engine
####################################################

    print("\n==============================")
    print("STAGE 8 : DECISION ENGINE")
    print("==============================")

    images = decide_images(images)

    print(f"Decision Engine Completed : {len(images)}")
    ####################################################
# Stage 9.1 : Caption Cleaner
####################################################

    print("\n==============================")
    print("STAGE 9.1 : CAPTION CLEANER")
    print("==============================")

    images = clean_captions(images)

    print(f"Caption Cleaner Completed : {len(images)}")
    ####################################################
# Stage 9.2 : OCR Cleaner
####################################################

    print("\n==============================")
    print("STAGE 9.2 : OCR CLEANER")
    print("==============================")

    images = clean_ocrs(images)

    print(f"OCR Cleaner Completed : {len(images)}")
    ####################################################
# Stage 9.3 : Metadata Normalizer
####################################################

    print("\n==============================")
    print("STAGE 9.3 : METADATA NORMALIZER")
    print("==============================")

    images = normalize_all_metadata(images)

    print(f"Metadata Normalized : {len(images)}") 
    ####################################################
# Stage 9.4 : Keyword Extractor
####################################################

    print("\n==============================")
    print("STAGE 9.4 : KEYWORD EXTRACTOR")
    print("==============================")

    images = extract_all_keywords(images)

    print(f"Keywords Extracted : {len(images)}")
    ####################################################
# Stage 9.5 : Search Text Builder
####################################################

    print("\n==============================")
    print("STAGE 9.5 : SEARCH TEXT")
    print("==============================")

    images = build_all_search_text(images)

    print(f"Search Text Built : {len(images)}")
    ####################################################
# Stage 10.1 : Embedding Generator
####################################################

    print("\n==============================")
    print("STAGE 10.1 : EMBEDDING GENERATOR")
    print("==============================")

    images = generate_embeddings(images)

    ####################################################
# Stage 10.2 : Embedding Validator
####################################################

    print("\n==============================")
    print("STAGE 10.2 : EMBEDDING VALIDATOR")
    print("==============================")

    images = validate_embeddings(images)

    print(f"Validated : {len(images)}")

    ####################################################
# Stage 10.3 : Vector Storage
####################################################
    print("Image vectors already stored in Stage 10.3 in upload_manager")
    ####################################################
# Stage 10.4 : Vector Verification
####################################################

    print("\n==============================")
    print("STAGE 10.4 : VECTOR VERIFIER")
    print("==============================")

    images = verify_vectors(images)

    print(f"Verified : {len(images)}")
    ####################################################
    # Pipeline Complete (Current Stage)
    ####################################################

    print("\n==============================")
    print("IMAGE PIPELINE COMPLETE")
    print("==============================")

    return images