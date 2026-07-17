from .layout_classifier import classify_layout


def classify_images(images):

    classified = 0

    for image in images:

        result = classify_layout(image.path)

        image.layout_class = result["label"]

        image.layout_confidence = result["confidence"]

        classified += 1

    print("\n==============================")
    print("DOCLAYOUT CLASSIFIER")
    print("==============================")
    print(f"Images Classified : {classified}")
    print("==============================")

    return images