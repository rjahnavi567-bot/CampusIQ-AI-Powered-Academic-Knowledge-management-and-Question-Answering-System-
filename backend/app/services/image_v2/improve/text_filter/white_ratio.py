import cv2
import numpy as np

WHITE_THRESHOLD = 245

MAX_WHITE_RATIO = 0.97


def white_ratio(crop):
    """
    Computes percentage of nearly-white pixels.
    """

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    white_pixels = np.sum(gray >= WHITE_THRESHOLD)

    total_pixels = gray.size

    ratio = white_pixels / total_pixels

    return ratio


def too_much_white(crop):

    ratio = white_ratio(crop)

    return {
        "white_ratio": ratio,
        "reject": ratio > MAX_WHITE_RATIO
    }