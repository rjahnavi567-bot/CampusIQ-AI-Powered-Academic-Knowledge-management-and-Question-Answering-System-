from PIL import Image

from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)

processor = (
    BlipProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )
)

model = (
    BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )
)

def generate_caption(
    image_path
):

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

    return processor.decode(
        output[0],
        skip_special_tokens=True
    )