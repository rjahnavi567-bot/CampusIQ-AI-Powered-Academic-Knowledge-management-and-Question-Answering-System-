import cv2
import numpy as np

from doclayout_yolo import YOLO

# =====================================================
# Load DocLayout model ONLY ONCE
# =====================================================

MODEL_PATH = r"models/doclayout/doclayout_yolo_docstructbench_imgsz1024.pt"

layout_model = YOLO(MODEL_PATH)


# =====================================================
# Classes that should become image candidates
# =====================================================

KEEP_CLASSES = {

    "figure",

    "table",

    "isolate_formula",

    "formula_caption"

}
# If later you also want captions:
# KEEP_CLASSES = {
#     "figure",
#     "table",
#     
# }


# =====================================================
# Detect figures using DocLayout
# =====================================================

def detect_figures(page_image):
    """
    Input:
        page_image (numpy BGR)

    Output:
        [
            {
                "bbox": (x1,y1,x2,y2),
                "category": "figure",
                "confidence": 0.97,
                "source": "doclayout"
            }
        ]
    """

    try:

        results = layout_model.predict(
            source=page_image,
            conf=0.25,
            verbose=False
        )

    except Exception as e:

        print("DocLayout Error:", e)
        return []

    result = results[0]

    detections = []

    for box in result.boxes:

        cls = int(box.cls.item())

        label = result.names[cls]

        if label not in KEEP_CLASSES:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if x2 <= x1 or y2 <= y1:
            continue

        confidence = float(box.conf.item())

        detections.append({

            "bbox": (
                x1,
                y1,
                x2,
                y2
            ),

            # keep compatibility with current pipeline
            "category": label,

            "confidence": confidence,

            "source": "doclayout"

        })

    print(f"DocLayout detected {len(detections)} useful objects.")

    return detections

def detect_figures_batch(images):

    """
    images = [
        numpy image,
        numpy image,
        ...
    ]

    returns

    [
        detections_for_page1,
        detections_for_page2,
        ...
    ]
    """

    results = layout_model.predict(

        source=images,

        conf=0.25,

        verbose=False

    )

    pages = []

    for result in results:

        page_detections = []

        for box in result.boxes:

            cls = int(box.cls.item())

            label = result.names[cls]

            if label not in KEEP_CLASSES:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            page_detections.append({

                "bbox": (x1,y1,x2,y2),

                "category": label,

                "confidence": float(box.conf.item()),

                "source":"doclayout"

            })

        pages.append(page_detections)

    return pages