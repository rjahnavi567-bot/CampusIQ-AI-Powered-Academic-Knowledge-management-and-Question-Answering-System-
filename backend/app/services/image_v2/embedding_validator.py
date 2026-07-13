import math


# --------------------------------------------------
# Validate One Embedding
# --------------------------------------------------

EXPECTED_DIMENSION = 384


def validate_embedding(image):

    image.embedding_valid = True
    image.embedding_error = ""

    embedding = getattr(image, "embedding", [])

    # -------------------------
    # Empty embedding
    # -------------------------

    if embedding is None or len(embedding) == 0:

        image.embedding_valid = False
        image.embedding_error = "Empty embedding"

        return image

    # -------------------------
    # Wrong dimension
    # -------------------------

    if len(embedding) != EXPECTED_DIMENSION:

        image.embedding_valid = False
        image.embedding_error = (

            f"Dimension {len(embedding)}"

        )

        return image

    # -------------------------
    # NaN / Infinite values
    # -------------------------

    for value in embedding:

        if math.isnan(value):

            image.embedding_valid = False
            image.embedding_error = "NaN value"

            return image

        if math.isinf(value):

            image.embedding_valid = False
            image.embedding_error = "Infinite value"

            return image

    return image


# --------------------------------------------------
# Validate All Images
# --------------------------------------------------

def validate_embeddings(images):

    print("\n==============================")
    print("STAGE 10.2 : EMBEDDING VALIDATOR")
    print("==============================")

    valid = 0
    invalid = 0

    for image in images:

        validate_embedding(image)

        if image.embedding_valid:

            valid += 1

        else:

            invalid += 1

    print(f"Valid   : {valid}")
    print(f"Invalid : {invalid}")

    print("\nSamples\n")

    for image in images[:5]:

        print(

            f"Page {image.page_no} | "

            f"Valid={image.embedding_valid} | "

            f"{image.embedding_error}"

        )

    return images