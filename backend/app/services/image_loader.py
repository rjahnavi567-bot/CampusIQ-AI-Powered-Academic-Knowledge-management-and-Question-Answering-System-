from PIL import Image
import os


MAX_IMAGE_SIZE = 1024


def load_image(image_path: str) -> Image.Image:
    """
    Loads an image safely for Vision models.

    - Converts to RGB
    - Resizes huge images
    - Returns PIL Image
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = Image.open(image_path)

    if image.mode != "RGB":
        image = image.convert("RGB")

    width, height = image.size

    longest_side = max(width, height)

    if longest_side > MAX_IMAGE_SIZE:

        scale = MAX_IMAGE_SIZE / longest_side

        new_width = int(width * scale)

        new_height = int(height * scale)

        image = image.resize(
            (new_width, new_height),
            Image.LANCZOS
        )

    return image