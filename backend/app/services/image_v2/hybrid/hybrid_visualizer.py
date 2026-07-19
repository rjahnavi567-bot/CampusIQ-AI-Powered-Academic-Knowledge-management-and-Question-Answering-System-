import cv2


def draw_boxes(image, boxes, save_path):

    img = image.copy()

    for box in boxes:

        x1, y1, x2, y2 = box["bbox"]

        label = box["label"]

        cv2.rectangle(
            img,
            (x1, y1),
            (x2, y2),
            (0,255,0),
            2
        )

        cv2.putText(
            img,
            label,
            (x1, y1-5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,0),
            2
        )

    cv2.imwrite(save_path, img)

    print("Saved:", save_path)