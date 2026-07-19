from doclayout_yolo import YOLO

MODEL = None


def load_model():

    global MODEL

    if MODEL is None:

        MODEL = YOLO(
            r"models/doclayout/doclayout_yolo_docstructbench_imgsz1024.pt"
        )

    return MODEL