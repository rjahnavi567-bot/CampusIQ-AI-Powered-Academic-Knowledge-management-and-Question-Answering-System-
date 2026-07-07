from concurrent.futures import ThreadPoolExecutor

from app.services.image_v2.classifier import classify_image


def worker(image):

    try:

        label, confidence = classify_image(

            image.path

        )

        image.category = label

        image.classification_confidence = confidence

    except Exception as e:

        print(e)

        image.category = "unknown"

        image.classification_confidence = 0.0

    return image


def classify_images(images):

    print("\nRunning CLIP Classification...")

    with ThreadPoolExecutor(max_workers=2) as executor:

        images = list(

            executor.map(

                worker,

                images

            )

        )

    print("Classification completed.")

    return images