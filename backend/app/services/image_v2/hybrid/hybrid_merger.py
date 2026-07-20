from typing import List


def iou(boxA, boxB):

    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    inter = max(0, xB - xA) * max(0, yB - yA)

    if inter == 0:
        return 0.0

    areaA = (boxA[2]-boxA[0]) * (boxA[3]-boxA[1])
    areaB = (boxB[2]-boxB[0]) * (boxB[3]-boxB[1])

    return inter / float(areaA + areaB - inter)

def merge_boxes(
    current_boxes: List[dict],
    doclayout_boxes: List[dict],
    threshold=0.50
):

    matched = []

    current_only = []

    doclayout_only = []

    used = set()

    for cur in current_boxes:

        best = None
        best_iou = 0

        for i, doc in enumerate(doclayout_boxes):

            if i in used:
                continue

            score = iou(
                cur["bbox"],
                doc["bbox"]
            )

            if score > best_iou:

                best_iou = score

                best = i

        if best is not None and best_iou >= threshold:

            matched.append({

                "current": cur,

                "doclayout": doclayout_boxes[best],

                "iou": best_iou

            })

            used.add(best)

        else:

            current_only.append(cur)

    for i, doc in enumerate(doclayout_boxes):

        if i not in used:

            doclayout_only.append(doc)

    return {

        "matched": matched,

        "current_only": current_only,

        "doclayout_only": doclayout_only

    }