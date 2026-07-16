from .ocr_density import is_text_heavy
from .connected_components import too_many_components
from .edge_density_filter import filter_edge_density
from .white_ratio import too_much_white
from .aspect_ratio import aspect_ratio_stats
from .quality_score import compute_quality_score
from app.services.image_v2.improve.positive_filter.photo_detector import detect_photo

from app.services.image_v2.improve.positive_filter.positive_score import compute_positive_score
def filter_text_heavy(page_image, detections):
    """
    Remove detections that are mostly text.
    """

    kept = []

    rejected = 0

    for det in detections:

        x1, y1, x2, y2 = det["bbox"]

        crop = page_image[y1:y2, x1:x2]
        if crop.size == 0:
            continue
        photo_stats = detect_photo(crop)

        det["is_photo"] = photo_stats["photo"]

        det["photo_confidence"] = photo_stats["confidence"]
        

        if crop.size == 0:
            continue

        result = is_text_heavy(crop)
        aspect_stats = aspect_ratio_stats(crop)
        component_stats = too_many_components(crop)
        edge_stats = filter_edge_density(crop)
        white_stats = too_much_white(crop)

        result["components"] = component_stats["components"]
        result["edge_density"] = edge_stats["edge_density"]
        

        result["white_ratio"] = white_stats["white_ratio"]
        result["aspect_ratio"] = aspect_stats["aspect_ratio"]

        quality = compute_quality_score(result)
        positive = compute_positive_score(det)

        quality["score"] = max(
    0,
    quality["score"] - positive["positive_score"]
)

        quality["reject"] = quality["score"] >= 5

        quality["reasons"].extend(
    positive["positive_reason"]
)

        result["quality_score"] = quality["score"]
        result["reject"] = quality["reject"]

        result["reject_reason"] = quality["reasons"]
        det["ocr_words"] = result["word_count"]
        det["ocr_chars"] = result["char_count"]
        det["text_ratio"] = result["text_ratio"]
        det["connected_components"] = result["components"]
        det["edge_density"] = result["edge_density"]
        det["white_ratio"] = result["white_ratio"]
        det["aspect_ratio"] = result["aspect_ratio"]
        result["is_photo"] = photo_stats["photo"]
        result["photo_confidence"] = photo_stats["confidence"]
        det["quality_score"] = result["quality_score"]
        det["reject_reason"] = result["reject_reason"]
        det["positive_score"] = positive["positive_score"]
        det["positive_reason"] = positive["positive_reason"]

        det["photo_confidence"] = photo_stats["confidence"]
        if result["reject"]:

            rejected += 1

            continue

        kept.append(det)

    print("\n==============================")
    print("TEXT FILTER")
    print("==============================")
    print(f"Rejected : {rejected}")
    print(f"Remaining : {len(kept)}")
    print("==============================")

    return kept