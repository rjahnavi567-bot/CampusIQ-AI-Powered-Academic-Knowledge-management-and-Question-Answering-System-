# --------------------------------------------------
# Validate One Image
# --------------------------------------------------

def validate_embedding(image):

    # -------------------------------
    # CLIP Validation
    # -------------------------------

    clip_ok = (
        hasattr(image, "clip_embedding")
        and image.clip_embedding is not None
        and len(image.clip_embedding) == 512
    )

    # -------------------------------
    # Text Validation
    # -------------------------------

    text_ok = (
        hasattr(image, "text_embedding")
        and image.text_embedding is not None
        and len(image.text_embedding) == 384
    )

    image.clip_valid = clip_ok
    image.text_valid = text_ok

    image.embedding_valid = clip_ok and text_ok

    return image


# --------------------------------------------------
# Batch Validation
# --------------------------------------------------

def validate_embeddings(images):

    print("\n==============================")
    print("STAGE 10.2 : EMBEDDING VALIDATOR")
    print("==============================")

    valid_images = []

    clip_success = 0
    text_success = 0

    for image in images:

        image = validate_embedding(image)

        if image.clip_valid:
            clip_success += 1

        if image.text_valid:
            text_success += 1

        if image.embedding_valid:
            valid_images.append(image)

    print(f"Total Images : {len(images)}")
    print(f"CLIP Valid   : {clip_success}")
    print(f"BGE Valid    : {text_success}")
    print(f"Images Kept  : {len(valid_images)}")

    print("\nSample Validation\n")

    for image in valid_images[:5]:

        print(
            f"Page {image.page_no} | "
            f"CLIP={len(image.clip_embedding)} | "
            f"BGE={len(image.text_embedding)}"
        )

    return valid_images