import os
import cv2
import numpy as np


# ---------------------------------------------------------
# Technical Validation Thresholds
# ---------------------------------------------------------

MIN_WIDTH = 40
MIN_HEIGHT = 40

MIN_AREA = 1600

MAX_WHITE_RATIO = 0.998
MAX_BLACK_RATIO = 0.998

MIN_BLUR = 3


# ---------------------------------------------------------
# Categories that bypass almost all heuristic filtering
# ---------------------------------------------------------

PROTECTED_CATEGORIES = {

    "diagram",
    "illustration",
    "flowchart",
    "chart",
    "graph",
    "medical image",
    "microscope image",
    "equipment",
    "device",
    "person",
    "animal",
    "map",
    "table",
    "equation",
    "book cover"

}


############################################################

def keep_image(image):

    if not os.path.exists(image.path):
        return False

    img = cv2.imread(image.path)

    if img is None:
        return False

    h, w = img.shape[:2]

    if h == 0 or w == 0:
        return False

    if w < MIN_WIDTH:
        return False

    if h < MIN_HEIGHT:
        return False

    if w * h < MIN_AREA:
        return False

    ##########################################################
    # Protected categories
    ##########################################################

    category = image.category.lower()

    if category in PROTECTED_CATEGORIES:

        return True

    ##########################################################
    # Remaining images undergo light validation
    ##########################################################

    gray = cv2.cvtColor(

        img,

        cv2.COLOR_BGR2GRAY

    )

    ##########################################################
    # Completely white image
    ##########################################################

    white_ratio = np.mean(gray > 250)

    if white_ratio > MAX_WHITE_RATIO:
        return False

    ##########################################################
    # Completely black image
    ##########################################################

    black_ratio = np.mean(gray < 5)

    if black_ratio > MAX_BLACK_RATIO:
        return False

    ##########################################################
    # Completely blurred / empty crop
    ##########################################################

    blur = cv2.Laplacian(

        gray,

        cv2.CV_64F

    ).var()

    if blur < MIN_BLUR:
        return False

    return True


############################################################

def filter_images(images):

    print("\n========== QUALITY FILTER ==========")

    kept = []

    removed = 0

    for image in images:

        try:

            if keep_image(image):

                kept.append(image)

            else:

                removed += 1

                try:

                    if os.path.exists(image.path):

                        os.remove(image.path)

                except Exception:
                    pass

        except Exception:

            removed += 1

    print(f"Input Images : {len(images)}")
    print(f"Kept         : {len(kept)}")
    print(f"Removed      : {removed}")
    print("====================================\n")

    return kept