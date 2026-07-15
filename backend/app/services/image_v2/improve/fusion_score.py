DETECTOR_PRIORITY = {
    "layout": 1.00,
    "region": 0.90,
    "visual": 0.80,
    "window": 0.70,
}


def assign_detection_scores(detections):

    for det in detections:

        source = det.get("source", "")

        detector_weight = DETECTOR_PRIORITY.get(source, 0.5)

        confidence = det.get("confidence", 0.5)

        det["fusion_score"] = (
            detector_weight * 0.7
            + confidence * 0.3
        )

    return detections