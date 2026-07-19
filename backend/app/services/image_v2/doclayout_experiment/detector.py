from .loader import load_model


def detect_layout(image_path):

    model = load_model()

    results = model.predict(
        source=image_path,
        conf=0.25,
        verbose=False
    )

    return results[0]