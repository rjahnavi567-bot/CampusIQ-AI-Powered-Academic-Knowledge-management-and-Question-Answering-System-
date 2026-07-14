from sentence_transformers import SentenceTransformer

bge_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def generate_text_embedding(text):

    embedding = bge_model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()