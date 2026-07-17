from concurrent.futures import ThreadPoolExecutor

from app.services.image_v2.caption_generator import generate_caption


def caption_images(images):

    from PIL import Image

    def worker(img):

        try:

        # Open image
            pil = Image.open(img.path)

            w, h = pil.size

        # Skip tiny images
            if w < 120 or h < 120:
                img.caption = ""
                img.caption_status = "skipped"
                return img
            

            img.caption = generate_caption(
            img.path
        )
            img.caption_status = "success"

        except Exception as e:

            print(e)

            img.caption = ""
            img.caption_status = "failed"
        

        return img

    with ThreadPoolExecutor(
        max_workers=2
    ) as executor:

        results = list(
            executor.map(worker, images)
        )

    return results