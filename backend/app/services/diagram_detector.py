import cv2
import numpy as np
import math
MIN_AREA = 35000

MIN_WIDTH = 180

MIN_HEIGHT = 180
MAX_TEXT_DENSITY = 0.42

MIN_GRAPHIC_DENSITY = 0.015

MIN_COMPONENTS = 8

def is_text_block(binary_crop):

    h, w = binary_crop.shape

    text_density = cv2.countNonZero(binary_crop) / (h * w)

    projection = np.sum(binary_crop > 0, axis=1)

    line_count = np.sum(

        projection > w * 0.35

    )

    return (

        text_density > MAX_TEXT_DENSITY

        and

        line_count > 10

    )

def has_graphics(binary_crop):
    """
    Returns True if crop has graphics/lines/boxes.
    """

    horizontal = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (40, 1)
    )

    vertical = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (1, 40)
    )

    h = cv2.morphologyEx(
        binary_crop,
        cv2.MORPH_OPEN,
        horizontal
    )

    v = cv2.morphologyEx(
        binary_crop,
        cv2.MORPH_OPEN,
        vertical
    )

    graphics = cv2.countNonZero(h) + cv2.countNonZero(v)

    return graphics > 500


def component_count(binary_crop):

    num_labels, _, _, _ = cv2.connectedComponentsWithStats(

        binary_crop,

        connectivity=8

    )

    return num_labels

def overlap_ratio(box1, box2):

    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    left = max(x1, x2)
    top = max(y1, y2)
    right = min(x1 + w1, x2 + w2)
    bottom = min(y1 + h1, y2 + h2)

    if right <= left or bottom <= top:
        return 0

    inter = (right - left) * (bottom - top)

    area1 = w1 * h1
    area2 = w2 * h2

    return inter / min(area1, area2)

def detect_diagrams(
    page_image_path,
    embedded_boxes=None
):
    if embedded_boxes is None:
        embedded_boxes = []

    image = cv2.imread(page_image_path)

    if image is None:
        return []

    original = image.copy()
    page_h, page_w = original.shape[:2]
    page_area = page_w * page_h

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )
    gray[:15, :] = 255

    gray[-15:, :] = 255

    gray[:, :15] = 255

    gray[:, -15:] = 255

    binary = cv2.adaptiveThreshold(

        gray,

        255,

        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

        cv2.THRESH_BINARY_INV,

        31,

        15

    )
    gray[:15, :] = 255

    gray[-15:, :] = 255

    gray[:, :15] = 255

    gray[:, -15:] = 255

    kernel = cv2.getStructuringElement(

        cv2.MORPH_RECT,

        (5, 5)

    )

    binary = cv2.dilate(

        binary,

        kernel,

        iterations=1

    )

    contours, _ = cv2.findContours(

        binary,

        cv2.RETR_EXTERNAL,

        cv2.CHAIN_APPROX_SIMPLE

    )

    diagrams = []

    used = []

    for contour in contours:

        x, y, w, h = cv2.boundingRect(contour)

        area = w * h
        # Ignore page-sized contour

        if area > page_area * 0.80:
            continue

        if area < MIN_AREA:
            continue

        if w < MIN_WIDTH:
            continue

        if h < MIN_HEIGHT:
            continue

        aspect = w / h

        if aspect > 8:
            continue

        if aspect < 0.12:
            continue

        skip = False

        for box in embedded_boxes:

            if overlap_ratio(
        (x, y, w, h),
        box
    ) > 0.40:

                skip = True
                break

        if skip:
            continue

        crop = original[y:y+h, x:x+w]

        crop_binary = binary[y:y+h, x:x+w]
        components = component_count( crop_binary)

        graphic_density = (

        cv2.countNonZero(crop_binary)

    /

    (w * h)

)

        # Ignore plain text paragraphs

        if is_text_block(crop_binary):

            if graphic_density > MAX_TEXT_DENSITY:

                continue

        if components < MIN_COMPONENTS:

            continue

        if (

    not has_graphics(crop_binary)

    and

    graphic_density < MIN_GRAPHIC_DENSITY

):

            continue

        duplicate = False

        for bx in used:

            xx, yy, ww, hh = bx

            inter_x = max(x, xx)

            inter_y = max(y, yy)

            inter_w = min(x+w, xx+ww) - inter_x

            inter_h = min(y+h, yy+hh) - inter_y

            if inter_w <= 0 or inter_h <= 0:
                continue

            inter = inter_w * inter_h

            union = w*h + ww*hh - inter

            if inter / union > 0.60:

                duplicate = True

                break

        if duplicate:
            continue

        used.append((x, y, w, h))

        diagrams.append({

            "image": crop,

            "bbox": (x, y, w, h)

        })
    print(

    f"Detected {len(diagrams)} diagram(s) "

    f"from {page_image_path}"

)

    return diagrams