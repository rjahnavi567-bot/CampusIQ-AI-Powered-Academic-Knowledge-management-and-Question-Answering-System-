import cv2
import torch
from PIL import Image

from .clip_model import (
    MODEL,
    PREPROCESS,
    DEVICE
)


# --------------------------------------------------
# Encode One Image
# --------------------------------------------------

def encode_image(image):

    img = cv2.imread(image.path)

    if img is None:
        return image

    img = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    )

    pil_image = Image.fromarray(img)

    image_tensor = PREPROCESS(pil_image)

    image_tensor = image_tensor.unsqueeze(0).to(DEVICE)

    with torch.no_grad():

        features = MODEL.encode_image(image_tensor)

    ##################################################
    # Normalize embedding
    ##################################################

    features = features / features.norm(
        dim=-1,
        keepdim=True
    )

    ##################################################
    # Save embedding
    ##################################################

    image.clip_embedding = (

        features[0]

        .cpu()

        .numpy()

        .tolist()

    )

    return image


# --------------------------------------------------
# Batch Encoding
# --------------------------------------------------

def encode_images(images):

    print("\n==============================")
    print("IMAGE ENCODER")
    print("==============================")

    total = len(images)

    for i, image in enumerate(images, 1):

        encode_image(image)

        if i % 25 == 0 or i == total:

            print(
                f"Encoded {i}/{total}"
            )

    print(
        f"\nImage embeddings generated : {total}"
    )

    return images