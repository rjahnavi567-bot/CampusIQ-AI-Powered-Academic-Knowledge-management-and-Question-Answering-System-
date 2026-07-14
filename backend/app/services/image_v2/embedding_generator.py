from app.services.image_embedding_service import (
    embed_image,
    embed_text_for_image_search
)

from app.services.image_models.text_model import (
    generate_text_embedding
)


# --------------------------------------------------
# Generate Query Embedding
# --------------------------------------------------

def generate_query_embedding(query: str):
    """
    Generate CLIP text embedding for image retrieval.
    Used during image search.
    """

    return embed_text_for_image_search(query)


# --------------------------------------------------
# Generate Embeddings for One Image
# --------------------------------------------------

def generate_embedding(image):
    """
    Generates BOTH:

    1. CLIP Image Embedding (512)
    2. BGE Text Embedding (384)
    """

    # ---------------------------------
    # CLIP Image Embedding
    # ---------------------------------

    try:

        image.clip_embedding = embed_image(image.path)

    except Exception as e:

        print(f"CLIP embedding failed : {image.path}")

        print(e)

        image.clip_embedding = []

    # ---------------------------------
    # BGE Text Embedding
    # ---------------------------------

    text = getattr(image, "search_text", "").strip()

    if text:

        try:

            image.text_embedding = generate_text_embedding(text)

        except Exception as e:

            print(f"BGE embedding failed : {image.path}")

            print(e)

            image.text_embedding = []

    else:

        image.text_embedding = []

    return image


# --------------------------------------------------
# Batch Embedding Generation
# --------------------------------------------------

def generate_embeddings(images):

    print("\n==============================")
    print("STAGE 10.1 : EMBEDDING GENERATOR")
    print("==============================")

    for image in images:

        generate_embedding(image)

    print(f"Embeddings Generated : {len(images)}")

    print("\nSample Embeddings\n")

    for image in images[:5]:

        clip_dim = len(image.clip_embedding) if image.clip_embedding else 0

        text_dim = len(image.text_embedding) if image.text_embedding else 0

        print(

            f"Page {image.page_no} | "

            f"CLIP = {clip_dim} | "

            f"BGE = {text_dim}"

        )

    return images