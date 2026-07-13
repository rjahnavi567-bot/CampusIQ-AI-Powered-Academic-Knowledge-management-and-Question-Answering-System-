
# --------------------------------------------------
# Process ONE image
# --------------------------------------------------

import cv2
import pytesseract


# --------------------------------------------------
# Process ONE image
# --------------------------------------------------

def process_image(image):

    img = cv2.imread(image.path)

    if img is None:

        image.ocr_text = ""
        image.word_count = 0
        image.text_area_ratio = 0.0
        image.line_count = 0
        image.bullet_count = 0

        return image

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    ####################################################
    # OCR TEXT
    ####################################################

    image.ocr_text = pytesseract.image_to_string(gray).strip()

    ####################################################
    # OCR DATA
    ####################################################

    data = pytesseract.image_to_data(
        gray,
        output_type=pytesseract.Output.DICT
    )

    words = []

    total_text_area = 0

    bullet_count = 0

    line_numbers = set()

    for i in range(len(data["text"])):

        text = data["text"][i].strip()

        if text == "":
            continue

        words.append(text)

        line_numbers.add(data["line_num"][i])

        w = data["width"][i]

        h = data["height"][i]

        total_text_area += w * h

        if text.startswith(("•", "-", "*")):

            bullet_count += 1

    image.word_count = len(words)

    image.line_count = len(line_numbers)

    image.bullet_count = bullet_count

    image.text_area_ratio = (

        total_text_area /

        max(image.area, 1)

    )

    return image
# --------------------------------------------------
# Process ALL images
# --------------------------------------------------

def compute_ocr_metadata(images):

    print("\n==============================")
    print("OCR METADATA")
    print("==============================")

    processed = []

    for image in images:

        processed.append(
            process_image(image)
        )

    print(f"OCR metadata computed for {len(processed)} images")

    print("\nSample OCR\n")

    for image in processed[:5]:

        print(f"Page {image.page_no}")

        print(image.ocr_text[:150])

        print()

        print(
        f"Words={image.word_count} | "
        f"Lines={image.line_count} | "
        f"Bullets={image.bullet_count}"
    )

        print("-" * 60)

    return processed