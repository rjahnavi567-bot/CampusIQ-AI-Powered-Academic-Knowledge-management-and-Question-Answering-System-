from PIL import Image
import torch

from app.services.image_v2.clip_model import (
    model,
    processor,
    DEVICE
)


# -------------------------------------------------------
# Categories used for routing
# -------------------------------------------------------

LABELS = [

    # Photographs
    "photograph",
    "person",
    "animal",
    "building",
    "natural scene",

    # Diagrams
    "flowchart",
    "block diagram",
    "architecture diagram",
    "network diagram",
    "uml diagram",
    "electrical circuit",
    "mechanical diagram",

    # Charts
    "line graph",
    "bar chart",
    "pie chart",
    "scatter plot",
    "histogram",

    # Tables
    "table",

    # Mathematics
    "equation",
    "mathematical formula",

    # Maps
    "map",

    # UI
    "user interface screenshot",

    # Scientific
    "microscope image",
    "medical image",

    # Logos
    "logo",

    # Books
    "book cover",

    # Document-like
    "text page",
    "paragraph",

    # Generic
    "illustration",
    "icon"
]


# -------------------------------------------------------
# Classifier
# -------------------------------------------------------

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

    label = LABELS[index]

    confidence = probs[0][index].item()

    return label, confidence