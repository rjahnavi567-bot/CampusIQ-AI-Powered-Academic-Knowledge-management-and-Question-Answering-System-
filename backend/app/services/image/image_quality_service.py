import cv2
import numpy as np


def image_entropy(gray):

    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

    hist = hist / hist.sum()

    hist = hist[hist > 0]

    return float(-(hist * np.log2(hist)).sum())


def edge_density(gray):

    edges = cv2.Canny(gray, 80, 180)

    return cv2.countNonZero(edges) / gray.size


def white_ratio(gray):

    return np.sum(gray > 245) / gray.size


def text_density(gray):

    binary = cv2.adaptiveThreshold(

        gray,

        255,

        cv2.ADAPTIVE_THRESH_MEAN_C,

        cv2.THRESH_BINARY_INV,

        31,

        15

    )

    horizontal = cv2.getStructuringElement(

        cv2.MORPH_RECT,

        (25, 1)

    )

    lines = cv2.morphologyEx(

        binary,

        cv2.MORPH_OPEN,

        horizontal

    )

    return cv2.countNonZero(lines) / gray.size


def is_good_embedded_image(image_path):

    image = cv2.imread(image_path)

    if image is None:

        return False

    gray = cv2.cvtColor(

        image,

        cv2.COLOR_BGR2GRAY

    )

    h, w = gray.shape

    area = h * w

    if area < 80000:

        return False

    aspect = w / h

    if aspect > 8 or aspect < 0.12:

        return False

    entropy = image_entropy(gray)

    if entropy < 2.2:

        return False

    edge = edge_density(gray)

    if edge < 0.005:

        return False

    if edge > 0.40:

        return False

    white = white_ratio(gray)

    if white > 0.97:

        return False

    text = text_density(gray)

    if text > 0.35:

        return False

    return True