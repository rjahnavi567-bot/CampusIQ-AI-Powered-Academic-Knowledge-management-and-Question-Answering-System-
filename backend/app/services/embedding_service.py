from sentence_transformers import SentenceTransformer

# Global embedding model
model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

def create_embedding(text):

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()


def create_embeddings(texts):

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=True
    )

    return embeddings