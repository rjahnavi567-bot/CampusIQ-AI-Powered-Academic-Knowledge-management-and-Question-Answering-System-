from PIL import Image
import torch

from .florence_loader import (
    load_florence,
    DEVICE
)

processor, model = load_florence()


def generate_captions(images):

    print("\n==============================")
    print("FLORENCE CAPTION GENERATOR")
    print("==============================")

    total = len(images)

    for index, image in enumerate(images, start=1):

        try:

            pil_image = Image.open(image.path).convert("RGB")

            task = "<MORE_DETAILED_CAPTION>"

            inputs = processor(
                text=task,
                images=pil_image,
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
                task=task,
                image_size=pil_image.size
            )

            image.florence_caption = parsed.get(task, "")

        except Exception as e:

            image.florence_caption = ""

            print(f"Caption failed : {image.path}")
            print(e)

        if index % 25 == 0 or index == total:

            print(f"Captioned {index}/{total}")

    return images