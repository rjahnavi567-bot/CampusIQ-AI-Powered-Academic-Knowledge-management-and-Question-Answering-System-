import cv2

MAX_EXPANSION = 80
STEP = 5

EDGE_THRESHOLD = 0.015


def edge_ratio(strip):

    if strip.size == 0:
        return 0

    gray = cv2.cvtColor(strip, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 80, 180)

    return edges.sum() / 255 / edges.size


def content_expand(box, image):

    height, width = image.shape[:2]

    x1, y1, x2, y2 = box

    expanded = True

    total_expand = 0

    while expanded and total_expand < MAX_EXPANSION:

        expanded = False

        # ---------------- Top ----------------

        if y1 - STEP >= 0:

            strip = image[y1 - STEP:y1, x1:x2]

            if edge_ratio(strip) > EDGE_THRESHOLD:

                y1 -= STEP

                expanded = True

        # ---------------- Bottom ----------------

        if y2 + STEP <= height:

            strip = image[y2:y2 + STEP, x1:x2]

            if edge_ratio(strip) > EDGE_THRESHOLD:

                y2 += STEP

                expanded = True

        # ---------------- Left ----------------

        if x1 - STEP >= 0:

            strip = image[y1:y2, x1 - STEP:x1]

            if edge_ratio(strip) > EDGE_THRESHOLD:

                x1 -= STEP

                expanded = True

        # ---------------- Right ----------------

        if x2 + STEP <= width:

            strip = image[y1:y2, x2:x2 + STEP]

            if edge_ratio(strip) > EDGE_THRESHOLD:

                x2 += STEP

                expanded = True

        total_expand += STEP

    return (
        max(0, x1),
        max(0, y1),
        min(width, x2),
        min(height, y2)
    )