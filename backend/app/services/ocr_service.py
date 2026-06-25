from PIL import Image
import pytesseract

def extract_ocr_text(
    image_path
):

    image = Image.open(
        image_path
    )

    return pytesseract.image_to_string(
        image
    )