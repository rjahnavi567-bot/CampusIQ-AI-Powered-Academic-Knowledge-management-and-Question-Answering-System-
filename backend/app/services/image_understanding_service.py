from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)

from PIL import Image
import easyocr

print("Loading BLIP model...")

processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

print("BLIP loaded")

print("Loading EasyOCR...")

reader = easyocr.Reader(
    ['en'],
    gpu=False
)

print("EasyOCR loaded")


def generate_caption(image_path):

    try:

        image = Image.open(
            image_path
        ).convert("RGB")

        inputs = processor(
            image,
            return_tensors="pt"
        )

        output = model.generate(
            **inputs,
            max_new_tokens=50
        )

        caption = processor.decode(
            output[0],
            skip_special_tokens=True
        )

        return caption

    except Exception as e:

        print(
            "Caption Error:",
            str(e)
        )

        return ""


def extract_ocr_text(image_path):

    try:

        results = reader.readtext(
            image_path,
            detail=0
        )

        return " ".join(results)

    except Exception as e:

        print(
            "OCR Error:",
            str(e)
        )

        return ""

import time

def understand_image(image_path):

    start = time.time()

    print(
        f"\nProcessing Image: "
        f"{image_path}"
    )

    caption = generate_caption(
        image_path
    )

    print(
        "Caption Done:",
        round(
            time.time()-start,
            2
        ),
        "sec"
    )

    ocr_text = extract_ocr_text(
        image_path
    )

    print(
        "OCR Done:",
        round(
            time.time()-start,
            2
        ),
        "sec"
    )

    return {

        "caption":
        caption,

        "ocr_text":
        ocr_text
    }