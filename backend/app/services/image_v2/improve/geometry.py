def area(box):
    """
    Compute bounding box area.

    box = (x1, y1, x2, y2)
    """

    x1, y1, x2, y2 = box

    return max(0, x2 - x1) * max(0, y2 - y1)


def iou(box1, box2):
    """
    Intersection over Union
    """

    ax1, ay1, ax2, ay2 = box1
    bx1, by1, bx2, by2 = box2

    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)

    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)

    inter_area = area(
        (
            inter_x1,
            inter_y1,
            inter_x2,
            inter_y2
        )
    )

    if inter_area == 0:
        return 0.0

    union = area(box1) + area(box2) - inter_area

    if union <= 0:
        return 0.0

    return inter_area / union