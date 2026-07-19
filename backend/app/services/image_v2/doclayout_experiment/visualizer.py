import cv2


def draw_boxes(result):

    image = result.orig_img.copy()

    for box in result.boxes:

        cls = result.names[int(box.cls)]

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0,255,0),
            2
        )

        cv2.putText(
            image,
            cls,
            (x1,y1-5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0,255,0),
            2
        )

    return image