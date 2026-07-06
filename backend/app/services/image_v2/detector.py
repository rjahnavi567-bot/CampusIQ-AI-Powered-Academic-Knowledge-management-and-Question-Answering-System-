import cv2

from ultralytics import YOLO


MODEL = YOLO(
    "models/doclayout/doclayout_yolo_docstructbench_imgsz1024.pt"
)


KEEP_CLASSES = {

    "Picture",

    "Table",

    "Formula"

}


def detect_layout(image_path):

    image = cv2.imread(image_path)

    h, w = image.shape[:2]

    results = MODEL.predict(

        source=image,

        conf=0.25,

        verbose=False

    )

    boxes = []

    for result in results:

        names = result.names

        for box in result.boxes:

            cls = int(box.cls.item())

            label = names[cls]

            if label not in KEEP_CLASSES:

                continue

            x1, y1, x2, y2 = map(

                int,

                box.xyxy[0]

            )

            boxes.append(

                {

                    "category": label,

                    "bbox": (

                        x1,

                        y1,

                        x2,

                        y2

                    ),

                    "confidence": float(

                        box.conf.item()

                    )

                }

            )

    return boxes