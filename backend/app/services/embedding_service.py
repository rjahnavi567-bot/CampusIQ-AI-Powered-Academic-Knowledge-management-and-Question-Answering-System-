from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def get_embedding(text):

    return model.encode(
        text,
        convert_to_numpy=True
    )


def get_embeddings(texts):

    return model.encode(
        texts,
        batch_size=32,
        convert_to_numpy=True,
        show_progress_bar=True
    )