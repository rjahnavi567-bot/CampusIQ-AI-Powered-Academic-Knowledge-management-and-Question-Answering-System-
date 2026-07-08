from .clip_model import MODEL
from .clip_model import PREPROCESS
from .clip_model import TOKENIZER
from .clip_model import DEVICE


def initialize_classifier():

    print("\n==============================")
    print("VISION CLASSIFIER")
    print("==============================")

    print("Model Ready")

    print(MODEL.visual)

    return True