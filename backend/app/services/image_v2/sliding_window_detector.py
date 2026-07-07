import cv2
from paddleocr import PPStructure


# --------------------------------------------------
# Sliding Window Configuration
# --------------------------------------------------

WINDOW_SIZE = 800
OVERLAP = 200


# --------------------------------------------------
# PPStructure
# --------------------------------------------------

layout_engine = PPStructure(
    show_log=False,
    layout=True,
    table=False,
    ocr=False
)


# --------------------------------------------------
# Generate Windows
# --------------------------------------------------

def generate_windows(page_image):

    height, width = page_image.shape[:2]

    windows = []

    stride = WINDOW_SIZE - OVERLAP

    for y in range(0, height, stride):

        for x in range(0, width, stride):

            x2 = min(x + WINDOW_SIZE, width)
            y2 = min(y + WINDOW_SIZE, height)

            crop = page_image[y:y2, x:x2]

            if crop.size == 0:
                continue

            windows.append(

                {

                    "image": crop,

                    "offset": (x, y)

                }

            )

    return windows


# --------------------------------------------------
# Detect Figures In Every Window
# --------------------------------------------------

def detect_window_figures(page_image):

    windows = generate_windows(page_image)

    recovered = []

    print(f"Sliding Windows : {len(windows)}")

    for window in windows:

        rgb = cv2.cvtColor(

            window["image"],

            cv2.COLOR_BGR2RGB

        )

        result = layout_engine(rgb)

        offset_x, offset_y = window["offset"]

        for item in result:

            if item["type"] != "figure":
                continue

            x1, y1, x2, y2 = map(
                int,
                item["bbox"]
            )

            ####################################################
            # Convert local coordinates to page coordinates
            ####################################################

            recovered.append(

                {

                    "bbox": (

                        x1 + offset_x,

                        y1 + offset_y,

                        x2 + offset_x,

                        y2 + offset_y

                    ),

                    "category": "window_figure",

                    "confidence": item.get(
                        "score",
                        1.0
                    )

                }

            )

    print(f"Recovered Figures : {len(recovered)}")

    return recovered