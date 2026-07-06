from PIL import Image
import torch

from app.services.image_v2.clip_model import (
    model,
    processor,
    DEVICE
)

LABELS = [
    "photograph",
    "table",
    "chart",
    "flowchart",
    "network diagram",
    "architecture diagram",
    "equation",
    "graph",
    "bar chart",
    "pie chart",
    "line chart",
    "scatter plot",
    "document",
    "user interface screenshot",
    "logo",
    "map"
]


def classify_image(image_path):

    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        text=LABELS,
        images=image,
        return_tensors="pt",
        padding=True
    )

    inputs = {
        k: v.to(DEVICE)
        for k, v in inputs.items()
    }

    with torch.no_grad():

        outputs = model(**inputs)

    probs = outputs.logits_per_image.softmax(dim=1)

    index = probs.argmax().item()

    return LABELS[index], probs[0][index].item()