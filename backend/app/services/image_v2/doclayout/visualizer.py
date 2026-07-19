import cv2


def draw_layout(results, save_path):

    result = results[0]

    image = result.orig_img.copy()

    boxes = result.boxes

    names = result.names

    for box in boxes:

        cls = int(box.cls.item())

        conf = float(box.conf.item())

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        label = f"{names[cls]} {conf:.2f}"

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            image,
            label,
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2
        )

    cv2.imwrite(save_path, image)

    print(f"\nSaved -> {save_path}")