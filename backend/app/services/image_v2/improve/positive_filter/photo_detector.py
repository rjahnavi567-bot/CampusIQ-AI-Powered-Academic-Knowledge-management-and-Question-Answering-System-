import cv2
import numpy as np


# ----------------------------------------
# Thresholds
# ----------------------------------------

MIN_COLOR_STD = 25

MIN_UNIQUE_COLORS = 500

MIN_EDGE_DENSITY = 0.02

MAX_EDGE_DENSITY = 0.20


def detect_photo(image):
    """
    Detect whether a crop is likely a natural photograph.

    Returns
    -------
    {
        "photo": bool,
        "confidence": float
    }
    """

    if image is None or image.size == 0:

        return {
            "photo": False,
            "confidence": 0.0
        }

    # ------------------------------------
    # Color variation
    # ------------------------------------

    color_std = np.mean(np.std(image.reshape(-1, 3), axis=0))

    # ------------------------------------
    # Unique colors
    # ------------------------------------

    pixels = image.reshape(-1, 3)

    unique_colors = len(np.unique(pixels, axis=0))

    # ------------------------------------
    # Edge density
    # ------------------------------------

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 80, 180)

    edge_density = np.count_nonzero(edges) / edges.size

    score = 0

    if color_std > MIN_COLOR_STD:
        score += 1

    if unique_colors > MIN_UNIQUE_COLORS:
        score += 1

    if MIN_EDGE_DENSITY < edge_density < MAX_EDGE_DENSITY:
        score += 1

    confidence = score / 3.0

    return {

        "photo": score >= 2,

        "confidence": confidence,

        "color_std": float(color_std),

        "unique_colors": int(unique_colors),

        "edge_density": float(edge_density)

    }