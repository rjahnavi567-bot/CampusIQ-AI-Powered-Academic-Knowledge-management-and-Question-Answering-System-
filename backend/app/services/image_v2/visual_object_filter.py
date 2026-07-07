import cv2
import numpy as np


# --------------------------------------------------
# Thresholds
# --------------------------------------------------

MIN_WIDTH = 120
MIN_HEIGHT = 120

MIN_AREA = 15000

MAX_ASPECT_RATIO = 8.0

MAX_WHITE_RATIO = 0.985

MIN_EDGE_RATIO = 0.003

MIN_VARIANCE = 120


# --------------------------------------------------
# Helper
# --------------------------------------------------

def keep_visual_object(page_image, detection):

    x1, y1, x2, y2 = map(int, detection["bbox"])

    crop = page_image[y1:y2, x1:x2]

    if crop.size == 0:
        return False

    h, w = crop.shape[:2]

    if w < MIN_WIDTH:
        return False

    if h < MIN_HEIGHT:
        return False

    if w * h < MIN_AREA:
        return False

    ratio = max(w / h, h / w)

    if ratio > MAX_ASPECT_RATIO:
        return False

    gray = cv2.cvtColor(
        crop,
        cv2.COLOR_BGR2GRAY
    )

    white_ratio = np.mean(gray > 245)

    if white_ratio > MAX_WHITE_RATIO:
        return False

    edges = cv2.Canny(
        gray,
        100,
        200
    )

    edge_ratio = np.count_nonzero(edges) / edges.size

    if edge_ratio < MIN_EDGE_RATIO:
        return False

    variance = gray.var()

    if variance < MIN_VARIANCE:
        return False

    return True


# --------------------------------------------------
# Batch Filter
# --------------------------------------------------

def filter_visual_objects(page_image, detections):

    filtered = []

    for det in detections:

        if keep_visual_object(page_image, det):

            filtered.append(det)

    print(f"Visual Objects After Filter : {len(filtered)}")

    return filtered