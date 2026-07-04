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