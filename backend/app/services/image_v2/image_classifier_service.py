from concurrent.futures import ThreadPoolExecutor

from app.services.image_v2.classifier import classify_image


def classify_images(images):

    def worker(img):

        try:
            label, score = classify_image(img.path)

            img.category = label
            img.classification_confidence = score

        except Exception as e:

            print(e)

            img.category = "figure"
            img.classification_confidence = 0

        return img

    with ThreadPoolExecutor(max_workers=2) as executor:

        images = list(
            executor.map(worker, images)
        )

    return images