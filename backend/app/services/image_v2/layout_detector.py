import cv2
from paddleocr import PPStructure


# ---------------------------------------------------
# PPStructure Layout Detector
# ---------------------------------------------------

layout_engine = PPStructure(
    layout=True,
    table=False,
    ocr=False,
    show_log=False
)


# ---------------------------------------------------
# Detect Figure Regions
# ---------------------------------------------------

def detect_figures(page_image):
    """
    Stage-2

    Input
    -----
    page_image : numpy.ndarray (BGR)

    Output
    ------
    [
        {
            "bbox": (x1,y1,x2,y2),
            "category": "figure",
            "confidence": 0.98,
            "source": "ppstructure"
        }
    ]
    """

    # PPStructure expects RGB image
    rgb = cv2.cvtColor(
        page_image,
        cv2.COLOR_BGR2RGB
    )

    try:
        results = layout_engine(rgb)

    except Exception as e:

        print("PPStructure Error :", e)

        return []

    detections = []

    for item in results:

        # Keep only figures
        if item.get("type") != "figure":
            continue

        try:

            x1, y1, x2, y2 = map(
                int,
                item["bbox"]
            )

            # Ignore invalid boxes
            if x2 <= x1 or y2 <= y1:
                continue

            detections.append(

                {

                    "bbox": (
                        x1,
                        y1,
                        x2,
                        y2
                    ),

                    "category": "figure",

                    "confidence": float(
                        item.get(
                            "score",
                            1.0
                        )
                    ),

                    "source": "ppstructure"

                }

            )

        except Exception:
            continue

    print(
        f"PPStructure detected {len(detections)} figure(s)."
    )

    return detections