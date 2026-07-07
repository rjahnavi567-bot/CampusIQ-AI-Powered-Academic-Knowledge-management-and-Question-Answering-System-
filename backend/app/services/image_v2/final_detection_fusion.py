from .region_fusion import calculate_iou


IOU_THRESHOLD = 0.35


def final_fusion(*detection_lists):
    """
    Merge detections from all detectors while removing duplicates.

    Input:
        final_fusion(
            layout,
            regions,
            windows,
            visual_objects
        )

    Output:
        Single detection list
    """

    merged = []

    for detections in detection_lists:

        for det in detections:

            duplicate = False

            for existing in merged:

                iou = calculate_iou(
                    det["bbox"],
                    existing["bbox"]
                )

                if iou >= IOU_THRESHOLD:

                    duplicate = True

                    # Keep the higher-confidence detection
                    if det.get("confidence", 0) > existing.get("confidence", 0):

                        existing["bbox"] = det["bbox"]
                        existing["category"] = det["category"]
                        existing["confidence"] = det["confidence"]

                    break

            if not duplicate:

                merged.append(det.copy())

    print(f"Final detections : {len(merged)}")

    return merged