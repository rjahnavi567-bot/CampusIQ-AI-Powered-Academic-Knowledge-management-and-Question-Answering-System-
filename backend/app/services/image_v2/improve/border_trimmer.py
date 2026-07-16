import cv2
import numpy as np


WHITE_THRESHOLD = 245

PADDING = 5


def trim_white_border(image):
    """
    Remove unnecessary white margins around a crop while
    preserving a small padding.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Everything darker than threshold is considered content
    mask = gray < WHITE_THRESHOLD

    if not np.any(mask):
        return image

    ys, xs = np.where(mask)

    x1 = max(0, xs.min() - PADDING)
    y1 = max(0, ys.min() - PADDING)

    x2 = min(image.shape[1], xs.max() + PADDING)
    y2 = min(image.shape[0], ys.max() + PADDING)

    return image[y1:y2, x1:x2]