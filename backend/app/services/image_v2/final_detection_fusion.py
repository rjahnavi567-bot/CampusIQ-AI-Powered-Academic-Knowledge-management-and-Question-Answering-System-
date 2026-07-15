from .improve.geometry import iou
from app.services.image_v2.improve.fusion_score import assign_detection_scores

IOU_THRESHOLD = 0.35


def final_fusion(*detection_lists):
    """
    Merge detections coming from

    layout
    region detector
    sliding window
    visual detector

    while removing duplicates.
    """

    # -----------------------------
    # Flatten all detections
    # -----------------------------

    all_boxes = []

    for detections in detection_lists:
        all_boxes.extend(detections)

    # -----------------------------
    # Assign detector priority score
    # -----------------------------

    all_boxes = assign_detection_scores(all_boxes)

    # -----------------------------
    # Sort best detections first
    # -----------------------------

    all_boxes.sort(
        key=lambda x: x.get("fusion_score", 0),
        reverse=True
    )

    merged = []

    # -----------------------------
    # Greedy fusion
    # -----------------------------

    for det in all_boxes:

        duplicate = False

        for existing in merged:

            io = iou(
                det["bbox"],
                existing["bbox"]
            )

            if io >= IOU_THRESHOLD:
                duplicate = True
                break

        if not duplicate:
            merged.append(det.copy())

    print(f"Final detections : {len(merged)}")

    return merged