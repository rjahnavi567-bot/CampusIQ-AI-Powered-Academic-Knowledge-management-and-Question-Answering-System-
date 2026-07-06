from PIL import Image

from app.services.image_v2.blip_model import (
    processor,
    model,
    DEVICE
)


def generate_caption(image_path):

    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        image,
        return_tensors="pt"
    ).to(DEVICE)

    output = model.generate(
        **inputs,
        max_new_tokens=40,
        num_beams=5,
        repetition_penalty=1.3,
        length_penalty=1.0,
        early_stopping=True
    )

    caption = processor.decode(
        output[0],
        skip_special_tokens=True
    )

    return caption.strip()