def boxes_close(box1, box2, gap=25):
    """
    Returns True if two boxes overlap or are very close.
    """

    x11, y11, x12, y12 = box1
    x21, y21, x22, y22 = box2

    return not (
        x12 + gap < x21 or
        x22 + gap < x11 or
        y12 + gap < y21 or
        y22 + gap < y11
    )


def merge_boxes(box1, box2):

    return (

        min(box1[0], box2[0]),
        min(box1[1], box2[1]),
        max(box1[2], box2[2]),
        max(box1[3], box2[3])

    )


def merge_visual_objects(detections):

    if len(detections) == 0:
        return []

    merged = []

    used = [False] * len(detections)

    for i in range(len(detections)):

        if used[i]:
            continue

        current = detections[i]["bbox"]

        used[i] = True

        changed = True

        while changed:

            changed = False

            for j in range(len(detections)):

                if used[j]:
                    continue

                if boxes_close(current, detections[j]["bbox"]):

                    current = merge_boxes(
                        current,
                        detections[j]["bbox"]
                    )

                    used[j] = True
                    changed = True

        merged.append({

            "bbox": current,

            "category": "visual_object",

            "confidence": 0.60

        })

    print(f"Merged Visual Objects : {len(merged)}")

    return merged