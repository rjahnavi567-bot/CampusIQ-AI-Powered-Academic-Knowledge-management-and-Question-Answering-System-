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


def detect_layout(image):

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

            crop = image[y1:y2, x1:x2]

            boxes.append(
{
    "category": label,
    "bbox": (x1, y1, x2, y2),
    "confidence": float(box.conf.item()),
    "crop": crop
}
)

    return boxes