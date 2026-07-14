from PIL import Image
from sentence_transformers import SentenceTransformer

clip_model = SentenceTransformer("clip-ViT-B-32")


def generate_clip_embedding(image_path):

    image = Image.open(image_path).convert("RGB")

    embedding = clip_model.encode(
        image,
        normalize_embeddings=True
    )

    return embedding.tolist()