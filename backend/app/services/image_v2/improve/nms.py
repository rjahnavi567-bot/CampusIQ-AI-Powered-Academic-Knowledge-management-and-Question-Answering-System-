from .geometry import iou


IOU_THRESHOLD = 0.45


def non_max_suppression(detections):
    """
    Keep highest-confidence detection when boxes overlap.
    """

    if len(detections) <= 1:
        return detections

    detections = sorted(
        detections,
        key=lambda d: d.get("fusion_score", 0),
        reverse=True
    )

    kept = []

    while detections:

        current = detections.pop(0)

        kept.append(current)

        remaining = []

        for det in detections:

            overlap = iou(
                current["bbox"],
                det["bbox"]
            )

            if overlap < IOU_THRESHOLD:
                remaining.append(det)

        detections = remaining

    print(f"NMS kept : {len(kept)}")

    return kept