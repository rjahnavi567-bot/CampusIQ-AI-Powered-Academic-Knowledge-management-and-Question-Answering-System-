"""
Stage 13.4.5
Figure Grouper

Purpose
-------
Merge detections that actually belong to one figure.

Example:

CPU box
Memory box
Arrow box

↓

Single Diagram

"""

import math

# ----------------------------------------------------------
# Parameters
# ----------------------------------------------------------

IOU_THRESHOLD = 0.20

CONTAIN_THRESHOLD = 0.90

HORIZONTAL_GAP = 50
VERTICAL_GAP = 50

ALIGNMENT_TOLERANCE = 40


# ----------------------------------------------------------
# Geometry
# ----------------------------------------------------------

def area(box):

    x1, y1, x2, y2 = box

    return max(0, x2 - x1) * max(0, y2 - y1)


def iou(box1, box2):

    ax1, ay1, ax2, ay2 = box1
    bx1, by1, bx2, by2 = box2

    x_left = max(ax1, bx1)
    y_top = max(ay1, by1)

    x_right = min(ax2, bx2)
    y_bottom = min(ay2, by2)

    if x_right <= x_left or y_bottom <= y_top:
        return 0.0

    inter = (x_right - x_left) * (y_bottom - y_top)

    union = area(box1) + area(box2) - inter

    if union == 0:
        return 0.0

    return inter / union


def merge_boxes(box1, box2):

    return (

        min(box1[0], box2[0]),

        min(box1[1], box2[1]),

        max(box1[2], box2[2]),

        max(box1[3], box2[3])

    )


# ----------------------------------------------------------
# Containment
# ----------------------------------------------------------

def containment_ratio(inner, outer):

    ix1, iy1, ix2, iy2 = inner
    ox1, oy1, ox2, oy2 = outer

    x_left = max(ix1, ox1)
    y_top = max(iy1, oy1)

    x_right = min(ix2, ox2)
    y_bottom = min(iy2, oy2)

    if x_right <= x_left or y_bottom <= y_top:
        return 0.0

    intersection = (x_right - x_left) * (y_bottom - y_top)

    if area(inner) == 0:
        return 0.0

    return intersection / area(inner)


# ----------------------------------------------------------
# Distance
# ----------------------------------------------------------

def box_distance(box1, box2):

    ax1, ay1, ax2, ay2 = box1
    bx1, by1, bx2, by2 = box2

    horizontal = max(bx1 - ax2, ax1 - bx2, 0)

    vertical = max(by1 - ay2, ay1 - by2, 0)

    return math.sqrt(horizontal ** 2 + vertical ** 2)


# ----------------------------------------------------------
# Alignment
# ----------------------------------------------------------

def vertically_aligned(box1, box2):

    ax1, ay1, ax2, ay2 = box1
    bx1, by1, bx2, by2 = box2

    cx1 = (ax1 + ax2) / 2
    cx2 = (bx1 + bx2) / 2

    return abs(cx1 - cx2) < ALIGNMENT_TOLERANCE


def horizontally_aligned(box1, box2):

    ax1, ay1, ax2, ay2 = box1
    bx1, by1, bx2, by2 = box2

    cy1 = (ay1 + ay2) / 2
    cy2 = (by1 + by2) / 2

    return abs(cy1 - cy2) < ALIGNMENT_TOLERANCE


# ----------------------------------------------------------
# Merge Decision
# ----------------------------------------------------------

def should_merge(det1, det2):

    box1 = det1["bbox"]
    box2 = det2["bbox"]

    # Rule 1
    if iou(box1, box2) >= IOU_THRESHOLD:
        return True

    # Rule 2
    if containment_ratio(box1, box2) >= CONTAIN_THRESHOLD:
        return True

    if containment_ratio(box2, box1) >= CONTAIN_THRESHOLD:
        return True

    # Rule 3
    distance = box_distance(box1, box2)

    if distance <= max(HORIZONTAL_GAP, VERTICAL_GAP):

        if vertically_aligned(box1, box2):
            return True

        if horizontally_aligned(box1, box2):
            return True

    return False


# ----------------------------------------------------------
# Merge Metadata
# ----------------------------------------------------------

def merge_detection_data(det1, det2):

    merged = det1.copy()

    merged["bbox"] = merge_boxes(
        det1["bbox"],
        det2["bbox"]
    )

    merged["confidence"] = max(
        det1.get("confidence", 0),
        det2.get("confidence", 0)
    )

    categories = set()

    if det1.get("category"):
        categories.add(det1["category"])

    if det2.get("category"):
        categories.add(det2["category"])

    merged["category"] = ",".join(sorted(categories))

    return merged


# ----------------------------------------------------------
# Main Function
# ----------------------------------------------------------

def group_figures(detections, image=None):

    if len(detections) <= 1:
        return detections

    detections = detections.copy()

    changed = True

    while changed:

        changed = False

        merged = []

        used = [False] * len(detections)

        for i in range(len(detections)):

            if used[i]:
                continue

            current = detections[i]

            for j in range(i + 1, len(detections)):

                if used[j]:
                    continue

                if should_merge(current, detections[j]):

                    current = merge_detection_data(
                        current,
                        detections[j]
                    )

                    used[j] = True

                    changed = True

            used[i] = True

            merged.append(current)

        detections = merged

    print(f"Figure Grouper : {len(detections)}")

    return detections