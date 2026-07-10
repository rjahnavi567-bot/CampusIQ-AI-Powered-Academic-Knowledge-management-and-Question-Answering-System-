import torch

from transformers import (
    AutoModelForCausalLM,
    AutoProcessor
)

MODEL_NAME = "microsoft/Florence-2-base-ft"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

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