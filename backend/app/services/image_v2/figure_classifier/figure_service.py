from .siglip_classifier import classify_figure


def classify_figures(images):

    classified = 0

    skipped = 0

    for image in images:

        if image.layout_class != "Figure":

            image.figure_type = ""

            image.figure_confidence = 0.0

            skipped += 1

            continue

        result = classify_figure(image.path)

        image.figure_type = result["figure_type"]

        image.figure_confidence = result["confidence"]

        classified += 1

    print("\n==============================")
    print("SIGLIP FIGURE CLASSIFIER")
    print("==============================")
    print(f"Figures Classified : {classified}")
    print(f"Skipped            : {skipped}")
    print("==============================")

    return images