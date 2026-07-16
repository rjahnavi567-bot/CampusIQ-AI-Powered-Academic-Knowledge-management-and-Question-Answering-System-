def contains(box1, box2):
    """
    True if box1 completely contains box2.
    """

    ax1, ay1, ax2, ay2 = box1
    bx1, by1, bx2, by2 = box2

    return (
        ax1 <= bx1 and
        ay1 <= by1 and
        ax2 >= bx2 and
        ay2 >= by2
    )


def remove_contained_boxes(detections):

    result = []

    for i, det in enumerate(detections):

        remove = False

        for j, other in enumerate(detections):

            if i == j:
                continue

            if contains(other["bbox"], det["bbox"]):

                if other.get("fusion_score", 0) >= det.get("fusion_score", 0):

                    remove = True

                    break

        if not remove:
            result.append(det)

    print(f"Containment filter : {len(result)}")

    return result