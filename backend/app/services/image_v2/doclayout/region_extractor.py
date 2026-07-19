import os
import cv2


def extract_regions(results, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    result = results[0]

    image = result.orig_img
    names = result.names
    counters = {}

    regions = []

    for box in result.boxes:

        cls = int(box.cls.item())

        label = names[cls]

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        crop = image[y1:y2, x1:x2]

        counters.setdefault(label, 0)
        counters[label] += 1

        filename = f"{label}_{counters[label]}.png"

        save_path = os.path.join(output_folder, filename)

        cv2.imwrite(save_path, crop)

        regions.append({

        "bbox": [x1, y1, x2, y2],

        "label": label,

        "path": save_path

    })

    print(f"Extracted {len(regions)} regions")

    return regions