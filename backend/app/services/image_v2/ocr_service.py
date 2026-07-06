from app.services.image_v2.ocr_model import ocr


def extract_ocr(image_path):

    try:

        result = ocr.ocr(
            image_path,
            cls=True
        )

        if result is None:
            return ""

        text = []

        for page in result:

            if page is None:
                continue

            for line in page:

                if line is None:
                    continue

                try:

                    txt = line[1][0].strip()

                    if txt:
                        text.append(txt)

                except Exception:
                    pass

        ocr_text = " ".join(text)

        words = ocr_text.split()

        if len(words) > 120:
            words = words[:120]

        return " ".join(words)

    except Exception as e:

        print("OCR Error:", e)

        return ""


# -----------------------------------
# NEW FUNCTION
# -----------------------------------

def run_ocr(images):

    print("\nRunning OCR...")

    for image in images:

        try:

            image.ocr_text = extract_ocr(
                image.path
            )

        except Exception as e:

            print(
                f"OCR failed: {image.path}"
            )

            print(e)

            image.ocr_text = ""

    print("OCR completed.")

    return images