import os
from app.services.image_embedding_service import (
    embed_images,
    embed_image
)


def generate_embeddings(images):

    image_paths = [
        img["path"]
        for img in images
    ]

    try:
        print()

        print("Embedding Images:")

        for img in image_paths:

            print(
        os.path.basename(img["path"])
    )

        print()

        embeddings = embed_images(image_paths)

    except Exception:

        embeddings = []

        for path in image_paths:

            try:
                embeddings.append(
                    embed_image(path)
                )

            except Exception:
                embeddings.append(None)

    for image, emb in zip(images, embeddings):

        image["clip_embedding"] = emb

    return images