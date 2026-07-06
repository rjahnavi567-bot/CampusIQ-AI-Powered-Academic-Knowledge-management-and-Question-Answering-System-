from transformers import CLIPProcessor
from transformers import CLIPModel

MODEL_NAME = "openai/clip-vit-base-patch32"

DEVICE = "cpu"

processor = CLIPProcessor.from_pretrained(
    MODEL_NAME
)

model = CLIPModel.from_pretrained(
    MODEL_NAME
)

model.to(DEVICE)

model.eval()