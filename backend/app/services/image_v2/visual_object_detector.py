import cv2
import numpy as np


MIN_OBJECT_AREA = 8000


def detect_visual_objects(page_image):

    gray = cv2.cvtColor(
        page_image,
        cv2.COLOR_BGR2GRAY
    )

    # Gradient image
    gradient = cv2.morphologyEx(
        gray,
        cv2.MORPH_GRADIENT,
        np.ones((3, 3), np.uint8)
    )

    _, binary = cv2.threshold(
        gradient,
        30,
        255,
        cv2.THRESH_BINARY
    )

    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (7, 7)
    )

    binary = cv2.morphologyEx(
        binary,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    detections = []

    for contour in contours:

        x, y, w, h = cv2.boundingRect(contour)

        area = w * h

        if area < MIN_OBJECT_AREA:
            continue

        detections.append({

            "bbox": (
                x,
                y,
                x + w,
                y + h
            ),

            "category": "visual_object",

            "confidence": 0.55

        })

    print(f"Visual Objects : {len(detections)}")

    return detections