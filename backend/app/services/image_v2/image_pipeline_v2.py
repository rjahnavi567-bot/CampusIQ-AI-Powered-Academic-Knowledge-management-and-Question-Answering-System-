import os
from .duplicate_scorer import score_duplicates
from .image_encoder import encode_images
from app.services.image_v2.extractor import ImageExtractor
from .duplicate_detector import detect_exact_duplicates
from app.services.image_v2.basic_crop_validator import filter_figures
from app.services.image_v2.duplicate_filter import remove_duplicates
from app.services.image_v2.quality_filter import filter_images
from app.services.image_v2.layout_metadata import analyze_layout
from .ocr_metadata import compute_ocr_metadata
from app.services.image_v2.caption_service import caption_images
from app.services.image_v2.ocr_service import run_ocr
from app.services.image_v2.quality_analyzer import analyze_quality
from app.services.image_v2.metadata_builder import build_all_metadata
from app.services.image_v2.embedding_pipeline import generate_embeddings
from app.services.image_v2.semantic_filter import filter_semantic
from app.services.image_v2.metadata_analyzer import analyze_metadata
from .duplicate_detector import (
    detect_exact_duplicates,
    detect_similar_duplicates
)
from .vision_scorer import score_vision
from .hard_rules import apply_hard_rules
from .decision_engine import decide_images
from .useful_score import compute_useful_scores
from .layout_scorer import score_layout
from .ocr_scorer import score_ocr
from .quality_scorer import score_quality
from .metadata_scorer import score_metadata
from .decision_initializer import initialize_decision
from .florence.florence_loader import load_florence

from .florence.florence_caption import generate_captions

from .florence.semantic_classifier import classify_images
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
    ####################################################
# Stage 5.2 : Similar Duplicate Detector
####################################################

    print("\n==============================")
    print("STAGE 5.2 : SIMILAR DUPLICATE")
    print("==============================")

    images = detect_similar_duplicates(images)

    print(f"Remaining Images : {len(images)}")
    #######################################
# Stage 6.1
#######################################

    print("\n==============================")
    print("STAGE 6.1 : LOAD FLORENCE")
    print("==============================")

    load_florence()
    #######################################
# Stage 6.2
#######################################

    print("\n==============================")
    print("STAGE 6.2 : GENERATE CAPTIONS") 
    print("==============================")

    images = generate_captions(images)

    print(f"Captions : {len(images)}")
    #######################################
# Stage 6.3
#######################################

    print("\n==============================")
    print("STAGE 6.3 : SEMANTIC CLASSIFIER")
    print("==============================")

    images = classify_images(images)

    print(f"Semantic : {len(images)}")
    print("\n==============================")
    print("STAGE 7.1 : DECISION MODEL")
    print("==============================")

    images = initialize_decision(images)

    print(
    f"Decision Model : {len(images)}"
)
    
    print("\n==============================")
    print("STAGE 7.2 : HARD RULES")
    print("==============================")

    images = apply_hard_rules(images)

    print(f"Hard Rules : {len(images)}")
    print("\n==============================")
    print("STAGE 7.3.1 : METADATA SCORE")
    print("==============================")

    images = score_metadata(images)

    print(f"Metadata Score : {len(images)}")
    print("\n==============================")
    print("STAGE 7.3.2 : QUALITY SCORE")
    print("==============================")

    images = score_quality(images)

    print(f"Quality Score : {len(images)}")
    print("\n==============================")
    print("STAGE 7.3.3 : OCR SCORE")
    print("==============================")

    images = score_ocr(images)

    print(f"OCR Score : {len(images)}")
    print("\n==============================")
    print("STAGE 7.3.4 : LAYOUT SCORE")
    print("==============================")

    images = score_layout(images)

    print(f"Layout Score : {len(images)}")
    print("\n==============================")
    print("STAGE 7.3.5 : VISION SCORE")
    print("==============================")

    images = score_vision(images)

    print(f"Vision Score : {len(images)}")
    print("\n==============================")
    print("STAGE 7.3.6 : DUPLICATE SCORE")
    print("==============================")

    images = score_duplicates(images)

    print(f"Duplicate Score : {len(images)}")
    print("\n==============================")
    print("STAGE 7.4 : USEFUL SCORE")
    print("==============================")

    images = compute_useful_scores(images)

    print(f"Useful Score : {len(images)}")
    print("\n==============================")
    print("STAGE 7.5 : FINAL DECISION")
    print("==============================")

    images = decide_images(images)

    print(f"Decision : {len(images)}")
    


    print("\n==============================")
    print("STAGE 2 : FIGURE FILTER")
    print("==============================")

    images = filter_figures(images)

    print(f"Remaining : {len(images)}")


    print("\n==============================")
    print("STAGE 3 : DUPLICATE REMOVAL")
    print("==============================")
    images = remove_duplicates(images)


    print(f"Remaining : {len(images)}")

    print("\n==============================")
    print("STAGE 5 : CLIP CLASSIFICATION")
    print("==============================")


    images = classify_images(images)
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
    

    images = filter_images(images)
    
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