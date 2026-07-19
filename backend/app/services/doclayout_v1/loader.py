from pathlib import Path

MODEL = None


def load_doclayout_model():
    """
    Loads DocLayout-YOLO only once.
    """

    global MODEL

    if MODEL is not None:
        return MODEL

    try:
        from doclayout_yolo import YOLO
    except ImportError:
        raise RuntimeError(
            "doclayout_yolo package is not installed."
        )

    model_path = (
        Path(__file__).resolve().parents[4]
        / "models"
        / "doclayout"
        / "doclayout_yolo_docstructbench_imgsz1024.pt"
    )

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found:\n{model_path}"
        )

    print("\n==============================")
    print("LOADING DOCLAYOUT-YOLO")
    print("==============================")
    print(model_path)

    MODEL = YOLO(str(model_path))

    print("\nModel Loaded Successfully.")

    return MODEL