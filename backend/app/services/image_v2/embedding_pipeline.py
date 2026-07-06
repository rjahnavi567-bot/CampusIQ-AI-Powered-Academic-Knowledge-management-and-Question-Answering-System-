from concurrent.futures import ThreadPoolExecutor

from app.services.image_v2.clip_service import embed_image


def generate_embeddings(images):

    def worker(img):

        img.clip_embedding = embed_image(

            img.path

        )

        return img

    with ThreadPoolExecutor(max_workers=2) as executor:

        images = list(

            executor.map(

                worker,

                images

            )

        )

    return images