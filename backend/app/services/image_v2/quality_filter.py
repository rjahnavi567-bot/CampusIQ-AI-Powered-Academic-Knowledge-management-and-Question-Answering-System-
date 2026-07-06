import cv2
import numpy as np


MIN_AREA = 50000

MIN_WIDTH = 180
MIN_HEIGHT = 180

MAX_TEXT_RATIO = 0.55

MAX_WHITE_RATIO = 0.96

MIN_EDGE_RATIO = 0.004


def keep_image(path):

    img = cv2.imread(path)

    if img is None:
        return False

    h, w = img.shape[:2]

    if w < MIN_WIDTH:
        return False

    if h < MIN_HEIGHT:
        return False

    if w * h < MIN_AREA:
        return False

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    white_ratio = np.mean(gray > 245)

    if white_ratio > MAX_WHITE_RATIO:
        return False
    
    aspect_ratio = max(w / h, h / w)

    if aspect_ratio > 6:
        return False
    
    blur = cv2.Laplacian(gray, cv2.CV_64F).var()

    if blur < 25:
        return False

    edges = cv2.Canny(
        gray,
        100,
        200
    )

    edge_ratio = np.count_nonzero(edges) / edges.size

    if edge_ratio < MIN_EDGE_RATIO:
        return False

    binary = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        25,
        15
    )

    text_ratio = np.count_nonzero(binary) / binary.size

    if text_ratio > MAX_TEXT_RATIO:
        return False

    return True

def filter_images(images):
    """
    Filters ImageCandidate objects.
    """

    filtered = []

    for image in images:

        if keep_image(image.path):
            filtered.append(image)

        else:
            try:
                import os

                if os.path.exists(image.path):
                    os.remove(image.path)

            except Exception:
                pass

    print(f"Quality Filter : {len(filtered)} images kept")

    return filtered