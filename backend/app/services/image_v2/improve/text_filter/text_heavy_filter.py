from .ocr_density import is_text_heavy
from .connected_components import too_many_components
from .edge_density_filter import filter_edge_density
from .white_ratio import too_much_white
from .aspect_ratio import aspect_ratio_stats

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

        result = is_text_heavy(crop)
        aspect_stats = aspect_ratio_stats(crop)
        component_stats = too_many_components(crop)
        edge_stats = filter_edge_density(crop)
        white_stats = too_much_white(crop)

        result["components"] = component_stats["components"]
        result["edge_density"] = edge_stats["edge_density"]
        

        result["white_ratio"] = white_stats["white_ratio"]
        result["aspect_ratio"] = aspect_stats["aspect_ratio"]

        if component_stats["reject"]:
            result["reject"] = True
        if edge_stats["reject"]:
            result["reject"] = True
        if white_stats["reject"]:
           result["reject"] = True
        
        if aspect_stats["reject"]:
           result["reject"] = True
        det["ocr_words"] = result["word_count"]
        det["ocr_chars"] = result["char_count"]
        det["text_ratio"] = result["text_ratio"]
        det["connected_components"] = result["components"]
        det["edge_density"] = result["edge_density"]
        det["white_ratio"] = result["white_ratio"]
        det["aspect_ratio"] = result["aspect_ratio"]
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