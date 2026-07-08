from PIL import Image
import torch

from app.services.image_v2.clip_model1 import model
from app.services.image_v2.clip_model1 import processor



def embed_text(text):

    inputs = processor(
        text=[text],
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():

        features = model.get_text_features(
            **inputs
        )

    features = features / features.norm(
        dim=-1,
        keepdim=True
    )

    return features[0].tolist()

def embed_image(image_path):

    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    with torch.no_grad():

        features = model.get_image_features(**inputs)

    features = features.squeeze()

    features = features / features.norm()

    return features.tolist()