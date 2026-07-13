from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# Load Embedding Model (Singleton)
# --------------------------------------------------

_model = None


def get_embedding_model():

    global _model

    if _model is None:

        print("Loading Image Embedding Model...")

        _model = SentenceTransformer(

    "BAAI/bge-small-en-v1.5"

)

    return _model

# --------------------------------------------------
# Generate Query Embedding
# --------------------------------------------------

def generate_query_embedding(query: str):

    model = get_embedding_model()

    vector = model.encode(
        query,
        normalize_embeddings=True
    )

    return vector.tolist()

# --------------------------------------------------
# Generate Embedding for One Image
# --------------------------------------------------

def generate_embedding(image, model):

    text = getattr(

        image,

        "search_text",

        ""

    )

    if text.strip() == "":

        image.embedding = []

        return image

    vector = model.encode(

        text,

        normalize_embeddings=True

    )

    image.embedding = vector.tolist()

    return image


# --------------------------------------------------
# Batch
# --------------------------------------------------

def generate_embeddings(images):

    print("\n==============================")
    print("STAGE 10.1 : EMBEDDING GENERATOR")
    print("==============================")

    model = get_embedding_model()

    for image in images:

        generate_embedding(

            image,

            model

        )

    print(f"Embeddings Generated : {len(images)}")

    print("\nSamples\n")

    for image in images[:5]:

        print(

            f"Page {image.page_no} | "

            f"Embedding Dimension = "

            f"{len(image.embedding)}"

        )

    return images