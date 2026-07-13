from .vector_storage import collection


# --------------------------------------------------
# Verify Stored Vectors
# --------------------------------------------------

def verify_vectors(images):

    print("\n==============================")
    print("STAGE 10.4 : VECTOR VERIFIER")
    print("==============================")

    verified = 0
    missing = 0

    samples = []

    for image in images:

        if not image.embedding_valid:
            continue

        image_id = image.vector_id

        result = collection.get(
            ids=[image_id],
            include=["documents", "metadatas", "embeddings"]
        )

        if len(result["ids"]) == 0:

            image.vector_verified = False
            missing += 1
            continue

        image.vector_verified = True

        verified += 1

        if len(samples) < 5:

            samples.append(

                (
                    image.page_no,
                    image.vector_id,
                    len(result["embeddings"][0]),
                    result["metadatas"][0]["layout"]
                )

            )

    print(f"Verified : {verified}")
    print(f"Missing  : {missing}")

    print("\nSamples\n")

    for page, vid, dim, layout in samples:

        print(

            f"Page {page} | "

            f"ID={vid} | "

            f"Dim={dim} | "

            f"{layout}"

        )

    return images