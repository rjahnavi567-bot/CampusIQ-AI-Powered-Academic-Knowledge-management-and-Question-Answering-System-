import os
import cv2


# --------------------------------------------------
# Basic Validation Thresholds
# --------------------------------------------------

MIN_WIDTH = 40
MIN_HEIGHT = 40
MIN_AREA = 1600


# --------------------------------------------------
# Image Validation
# --------------------------------------------------

def keep_figure(image):

    # File must exist
    if not os.path.exists(image.path):
        return False

    img = cv2.imread(image.path)

    if img is None:
        return False

    h, w = img.shape[:2]

    # Empty image
    if h == 0 or w == 0:
        return False

    # Too small
    if w < MIN_WIDTH:
        return False

    if h < MIN_HEIGHT:
        return False

    # Too tiny
    if w * h < MIN_AREA:
        return False

    return True


# --------------------------------------------------
# Batch Validation
# --------------------------------------------------

def filter_figures(images):

    print("\n========== BASIC CROP VALIDATION ==========")

    accepted = []
    removed = 0

    for image in images:

        try:

            if keep_figure(image):

                accepted.append(image)

            else:

                removed += 1

                try:
                    if os.path.exists(image.path):
                        os.remove(image.path)
                except Exception:
                    pass

        except Exception:

            removed += 1

            try:
                if os.path.exists(image.path):
                    os.remove(image.path)
            except Exception:
                pass

    print(f"Input Images : {len(images)}")
    print(f"Accepted     : {len(accepted)}")
    print(f"Rejected     : {removed}")
    print("==========================================\n")

    return accepted