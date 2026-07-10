import torch

from transformers import (
    AutoProcessor,
    AutoModelForCausalLM
)

MODEL_NAME = "microsoft/Florence-2-base-ft"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

processor = None
model = None


def load_florence():

    global processor
    global model

    if processor is not None and model is not None:
        return processor, model

    print("\n==============================")
    print("LOADING FLORENCE-2")
    print("==============================")

    processor = AutoProcessor.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True
    )

    model.to(DEVICE)
    model.eval()

    print()
    print("Florence Loaded Successfully")
    print(f"Device : {DEVICE}")
    print(f"Model  : {MODEL_NAME}")

    return processor, model