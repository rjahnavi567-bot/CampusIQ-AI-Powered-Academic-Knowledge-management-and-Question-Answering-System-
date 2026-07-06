from concurrent.futures import ThreadPoolExecutor

from app.services.image_v2.caption_generator import generate_caption


def caption_images(images):

    def worker(img):

        try:

            img["caption"] = generate_caption(
                img["path"]
            )

        except Exception as e:

            print(e)

            img["caption"] = ""

        return img

    with ThreadPoolExecutor(
        max_workers=2
    ) as executor:

        results = list(
            executor.map(worker, images)
        )

    return results