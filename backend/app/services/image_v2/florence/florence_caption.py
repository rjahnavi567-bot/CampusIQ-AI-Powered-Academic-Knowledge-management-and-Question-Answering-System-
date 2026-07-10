from PIL import Image

import torch
from .florence_loader import (
    load_florence,
    DEVICE
)
processor, model = load_florence()
def generate_captions(image_path):

    image = Image.open(image_path).convert("RGB")

    prompt = "<MORE_DETAILED_CAPTION>"

    inputs = processor(
        text=prompt,
        images=image,
        return_tensors="pt"
    )

    inputs = {
        k: v.to(DEVICE)
        for k, v in inputs.items()
    }

    with torch.no_grad():

        generated_ids = model.generate(

            input_ids=inputs["input_ids"],

            pixel_values=inputs["pixel_values"],

            max_new_tokens=128,

            num_beams=3,

            do_sample=False

        )

    generated_text = processor.batch_decode(

        generated_ids,

        skip_special_tokens=False

    )[0]

    parsed = processor.post_process_generation(

        generated_text,

        task=prompt,

        image_size=image.size

    )

    return parsed[prompt]