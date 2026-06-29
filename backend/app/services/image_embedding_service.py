from PIL import Image
from sentence_transformers import SentenceTransformer

# CLIP model (512-dimensional embeddings)
clip_model = SentenceTransformer("clip-ViT-B-32")


def embed_image(image_path):
    """
    Generate a 512-dimensional embedding for an image.
    """
    image = Image.open(image_path).convert("RGB")
    embedding = clip_model.encode(image)
    return embedding.tolist()


def embed_text_for_image_search(text):
    """
    Convert a user's question into the same 512-dimensional
    CLIP embedding space as stored images.
    """
    embedding = clip_model.encode(text)
    return embedding.tolist()