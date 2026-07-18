from transformers import AutoProcessor
from transformers import AutoModelForZeroShotImageClassification

MODEL = None
PROCESSOR = None


def load_siglip():

    global MODEL
    global PROCESSOR

    if MODEL is None:

        print("Loading SigLIP...")

        PROCESSOR = AutoProcessor.from_pretrained(
            "google/siglip-base-patch16-224"
        )

        MODEL = AutoModelForZeroShotImageClassification.from_pretrained(
            "google/siglip-base-patch16-224"
        )

        print("SigLIP Loaded")

    return MODEL, PROCESSOR