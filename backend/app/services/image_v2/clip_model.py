import torch
import open_clip


print("\nLoading CLIP Model...")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MODEL, _, PREPROCESS = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="laion2b_s34b_b79k"
)

MODEL = MODEL.to(DEVICE)

TOKENIZER = open_clip.get_tokenizer("ViT-B-32")

print(f"CLIP Loaded on {DEVICE}")