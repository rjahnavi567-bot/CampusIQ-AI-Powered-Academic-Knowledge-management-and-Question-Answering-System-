def calculate_iou(box1, box2):

    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])

    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    if x2 <= x1 or y2 <= y1:
        return 0.0

    intersection = (x2 - x1) * (y2 - y1)

    area1 = (
        (box1[2] - box1[0]) *
        (box1[3] - box1[1])
    )

    area2 = (
        (box2[2] - box2[0]) *
        (box2[3] - box2[1])
    )

    union = area1 + area2 - intersection

    if union <= 0:
        return 0.0

    return intersection / union


############################################################


IOU_THRESHOLD = 0.50


def merge_window_detections(

    page_detections,

    window_detections

):

    merged = list(page_detections)

    added = 0

    for window_box in window_detections:

        duplicate = False

        for page_box in merged:

            iou = calculate_iou(

                page_box["bbox"],

                window_box["bbox"]

            )

            if iou >= IOU_THRESHOLD:

                duplicate = True
                break

        if not duplicate:

            merged.append(window_box)

            added += 1

    print(f"Recovered new figures : {added}")

    print(f"Final detections : {len(merged)}")

    return merged