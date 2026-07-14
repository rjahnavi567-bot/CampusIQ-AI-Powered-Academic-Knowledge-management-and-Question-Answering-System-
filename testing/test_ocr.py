import os

from app.services.image_v2.ocr_service import extract_ocr

folder = "layout_output"

files = sorted(os.listdir(folder))

for file in files[:10]:

    path = os.path.join(folder, file)

    print("=" * 80)

    print(file)

    print()

    text = extract_ocr(path)

    print(text)

    print()