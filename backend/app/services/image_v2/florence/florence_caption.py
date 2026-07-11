
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from .florence_loader import (
    load_florence,
    DEVICE
)
import torch
import os
torch.set_num_threads(os.cpu_count())
BATCH_SIZE = 8
def load_image(path):
    """
    Loads a single image.
    """

    try:
        return Image.open(path).convert("RGB")

    except Exception:

        return None
def generate_captions(
    images,
    processor,
    model
):

    print("\n==============================")
    print("FLORENCE CAPTION GENERATOR")
    print("==============================")

    total = len(images)

    for start in range(0, total, BATCH_SIZE):

        batch = images[start:start + BATCH_SIZE]

        #
        # Load images in parallel
        #

        with ThreadPoolExecutor(max_workers=4) as executor:

            pil_images = list(
                executor.map(
                    lambda x: load_image(x.path),
                    batch
                )
            )

        #
        # Remove failed images
        #

        valid = []

        valid_images = []

        for img_obj, pil in zip(batch, pil_images):

            if pil is not None:

                valid.append(pil)

                valid_images.append(img_obj)

            else:

                img_obj.florence_caption = ""

        if len(valid) == 0:
            continue

        #
        # Florence prompt
        #

        task = "<MORE_DETAILED_CAPTION>"

        inputs = processor(

            text=[task] * len(valid),

            images=valid,

            return_tensors="pt",

            padding=True

        )

        inputs = {

            k: v.to(DEVICE)

            for k, v in inputs.items()

        }

        #
        # Generate captions
        #

        with torch.no_grad():

            generated_ids = model.generate(

                input_ids=inputs["input_ids"],

                pixel_values=inputs["pixel_values"],

                max_new_tokens=64,

                num_beams=1,

                do_sample=False

            )

        decoded = processor.batch_decode(

            generated_ids,

            skip_special_tokens=False

        )

        #
        # Parse captions
        #

        for img_obj, pil, text in zip(

            valid_images,

            valid,

            decoded

        ):

            parsed = processor.post_process_generation(

                text,

                task=task,

                image_size=pil.size

            )

            img_obj.florence_caption = parsed.get(task, "")

        end = min(start + BATCH_SIZE, total)

        print(f"Captioned {end}/{total}")

    return images