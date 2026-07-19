import cv2
import os

USEFUL_CLASSES = {

    "figure",
    "table",
    "isolate_formula"

}


def extract_regions(result, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    image = result.orig_img

    saved = []

    for i, box in enumerate(result.boxes):

        cls = result.names[int(box.cls)]

        if cls not in USEFUL_CLASSES:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        crop = image[y1:y2, x1:x2]

        path = os.path.join(
            output_dir,
            f"{cls}_{i}.png"
        )

        cv2.imwrite(path, crop)

        saved.append(path)

    return saved