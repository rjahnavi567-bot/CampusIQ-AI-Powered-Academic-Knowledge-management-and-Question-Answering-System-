import torch
from PIL import Image

from .loader import load_siglip


LABELS = [

    "paragraph of text",

    "page full of text",

    "bullet list",

    "heading",

    "flowchart",

    "block diagram",

    "scientific illustration",

    "graph",

    "bar chart",

    "line chart",

    "pie chart",

    "table",

    "photograph",

    "chemical structure",

    "electrical circuit",

    "biology diagram"

]


def classify_image(image_path):

    model, processor = load_siglip()

    image = Image.open(image_path).convert("RGB")

    inputs = processor(

        text=LABELS,

        images=image,

        padding=True,

        return_tensors="pt"

    )

    with torch.no_grad():

        outputs = model(**inputs)

    probs = outputs.logits_per_image.softmax(dim=1)

    best = probs.argmax().item()

    return {

        "label": LABELS[best],

        "confidence": float(probs[0][best])

    }