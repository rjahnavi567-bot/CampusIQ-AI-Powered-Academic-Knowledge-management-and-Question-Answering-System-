import cv2
import numpy as np


# ---------------------------------------------------------
# Utility
# ---------------------------------------------------------

def edge_density(gray):

    edges = cv2.Canny(gray, 80, 180)

    return cv2.countNonZero(edges) / gray.size


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

        (30, 1)

    )

    lines = cv2.morphologyEx(

        binary,

        cv2.MORPH_OPEN,

        horizontal

    )

    return cv2.countNonZero(lines) / gray.size


def component_count(gray):

    binary = cv2.adaptiveThreshold(

        gray,

        255,

        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

        cv2.THRESH_BINARY_INV,

        31,

        15

    )

    num_labels, _, _, _ = cv2.connectedComponentsWithStats(

        binary,

        connectivity=8

    )

    return num_labels


def has_long_lines(gray):

    edges = cv2.Canny(gray, 50, 150)

    lines = cv2.HoughLinesP(

        edges,

        1,

        np.pi / 180,

        threshold=80,

        minLineLength=80,

        maxLineGap=10

    )

    if lines is None:

        return False

    return len(lines) >= 5


# ---------------------------------------------------------
# Academic Figure Detector
# ---------------------------------------------------------

def is_academic_figure(image_path):

    image = cv2.imread(image_path)

    if image is None:

        return False

    gray = cv2.cvtColor(

        image,

        cv2.COLOR_BGR2GRAY

    )

    h, w = gray.shape

    area = h * w

    if area < 60000:

        return False

    edge = edge_density(gray)

    text = text_density(gray)

    components = component_count(gray)

    lines = has_long_lines(gray)

    std = np.std(gray)

    white = np.sum(gray > 245) / area

    score = 0

    # -------------------------------------------------
    # Structure
    # -------------------------------------------------

    if edge > 0.01:

        score += 1

    if edge < 0.35:

        score += 1

    if components > 20:

        score += 1

    if lines:

        score += 2

    if std > 18:

        score += 1

    if white < 0.98:

        score += 1

    # -------------------------------------------------
    # Reject text pages
    # -------------------------------------------------

    if text > 0.28:

        score -= 3

    if edge > 0.45:

        score -= 2
    accepted = score >= 4

    print(
    f"[Figure Detector] "
    f"{image_path} | "
    f"Score={score} "
    f"Edge={edge:.3f} "
    f"Text={text:.3f} "
    f"Components={components} "
    f"Lines={lines} "
    f"=> {'ACCEPT' if accepted else 'REJECT'}"
)

    return accepted
