import cv2
import numpy as np

MIN_AREA = 35000

MIN_WIDTH = 180

MIN_HEIGHT = 180


def is_text_block(binary_crop):
    """
    Returns True if crop mostly contains text.
    """

    h_projection = np.sum(binary_crop > 0, axis=1)

    line_count = np.sum(h_projection > binary_crop.shape[1] * 0.35)

    return line_count > 12


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


def detect_diagrams(page_image_path):

    image = cv2.imread(page_image_path)

    if image is None:
        return []

    original = image.copy()

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    binary = cv2.adaptiveThreshold(

        gray,

        255,

        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

        cv2.THRESH_BINARY_INV,

        31,

        15

    )

    kernel = cv2.getStructuringElement(

        cv2.MORPH_RECT,

        (9, 9)

    )

    binary = cv2.dilate(

        binary,

        kernel,

        iterations=2

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

        crop = original[y:y+h, x:x+w]

        crop_binary = binary[y:y+h, x:x+w]

        # Ignore plain text paragraphs

        if is_text_block(crop_binary):

            if not has_graphics(crop_binary):

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

    return diagrams