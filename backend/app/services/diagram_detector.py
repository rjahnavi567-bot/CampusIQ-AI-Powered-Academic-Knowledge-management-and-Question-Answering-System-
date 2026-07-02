import cv2
import numpy as np


MIN_COMPONENT_AREA = 2500

MIN_DIAGRAM_AREA = 35000

MIN_WIDTH = 180

MIN_HEIGHT = 180


def detect_diagrams(page_image_path):
    """
    Detect diagrams, graphs, flowcharts, screenshots,
    tables and large figures from an entire rendered page.

    Returns
    -------
    list
        [
            {
                "image": cropped_image,
                "bbox": (x, y, w, h)
            }
        ]
    """

    page = cv2.imread(page_image_path)

    if page is None:
        return []

    original = page.copy()

    gray = cv2.cvtColor(page, cv2.COLOR_BGR2GRAY)

    # ----------------------------------------
    # Adaptive Threshold
    # ----------------------------------------

    thresh = cv2.adaptiveThreshold(

        gray,

        255,

        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

        cv2.THRESH_BINARY_INV,

        31,

        15

    )

    # ----------------------------------------
    # Connect nearby components
    # ----------------------------------------

    kernel = cv2.getStructuringElement(

        cv2.MORPH_RECT,

        (9, 9)

    )

    thresh = cv2.dilate(

        thresh,

        kernel,

        iterations=2

    )

    # ----------------------------------------
    # Connected Components
    # ----------------------------------------

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(

        thresh,

        connectivity=8

    )

    detected = []

    used_boxes = []

    for i in range(1, num_labels):

        x = stats[i, cv2.CC_STAT_LEFT]

        y = stats[i, cv2.CC_STAT_TOP]

        w = stats[i, cv2.CC_STAT_WIDTH]

        h = stats[i, cv2.CC_STAT_HEIGHT]

        area = stats[i, cv2.CC_STAT_AREA]

        if area < MIN_COMPONENT_AREA:
            continue

        if w < MIN_WIDTH:
            continue

        if h < MIN_HEIGHT:
            continue

        if w * h < MIN_DIAGRAM_AREA:
            continue

        crop = original[y:y+h, x:x+w]

        if crop.size == 0:
            continue

        duplicate = False

        for bx in used_boxes:

            xx, yy, ww, hh = bx

            inter_x = max(x, xx)

            inter_y = max(y, yy)

            inter_w = min(x+w, xx+ww) - inter_x

            inter_h = min(y+h, yy+hh) - inter_y

            if inter_w <= 0 or inter_h <= 0:
                continue

            inter_area = inter_w * inter_h

            union = w*h + ww*hh - inter_area

            iou = inter_area / union

            if iou > 0.55:
                duplicate = True
                break

        if duplicate:
            continue

        used_boxes.append((x, y, w, h))

        detected.append({

            "image": crop,

            "bbox": (x, y, w, h)

        })

    return detected