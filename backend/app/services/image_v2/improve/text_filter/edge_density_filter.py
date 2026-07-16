import cv2
import numpy as np

LOW_EDGE_THRESHOLD = 0.015
HIGH_EDGE_THRESHOLD = 0.35


def edge_density(image):
    """
    Calculate edge density of one cropped image.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(
        gray,
        80,
        180
    )

    density = np.count_nonzero(edges) / edges.size

    return density


def filter_edge_density(crop):
    """
    Returns statistics for one crop.
    """

    density = edge_density(crop)

    reject = False

    if density < LOW_EDGE_THRESHOLD:
        reject = True

    if density > HIGH_EDGE_THRESHOLD:
        reject = True

    return {
        "edge_density": density,
        "reject": reject
    }