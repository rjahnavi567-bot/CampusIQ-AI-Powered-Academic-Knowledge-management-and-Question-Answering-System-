from PIL import Image
from sentence_transformers import SentenceTransformer

# Load only once
clip_model = SentenceTransformer("clip-ViT-B-32")


def embed_image(image_path):
    """
    Backward-compatible function.
    Used anywhere a single embedding is needed.
    """

    image = Image.open(image_path).convert("RGB")

    embedding = clip_model.encode(
        image,
        normalize_embeddings=True
    )

    return embedding.tolist()


def embed_images(image_paths):
    """
    Batch-generate CLIP embeddings.

    Returns:
        List[List[float]]
    """

    images = []

    valid_indices = []

    for idx, path in enumerate(image_paths):

        try:

            img = Image.open(path).convert("RGB")

            images.append(img)

            valid_indices.append(idx)

        except Exception:

            images.append(None)

    valid_images = [

        img for img in images

        if img is not None

    ]

    if not valid_images:

        return [None] * len(image_paths)

    embeddings = clip_model.encode(

        valid_images,

        batch_size=16,

        normalize_embeddings=True,

        show_progress_bar=False

    )

    results = [None] * len(image_paths)

    j = 0

    for i in valid_indices:

        results[i] = embeddings[j].tolist()

        j += 1

    return results


def embed_text_for_image_search(text):

    embedding = clip_model.encode(

        text,

        normalize_embeddings=True

    )

    return embedding.tolist()