def verify_vectors(images):

    print("\n==============================")
    print("STAGE 10.4 : VECTOR VERIFIER")
    print("==============================")

    valid = 0

    for image in images:

        text_ok = (
            hasattr(image, "text_embedding")
            and image.text_embedding
            and len(image.text_embedding) == 384
        )

        clip_ok = (
            hasattr(image, "clip_embedding")
            and image.clip_embedding
            and len(image.clip_embedding) == 512
        )

        if text_ok and clip_ok:
            valid += 1

    print(f"Verified : {valid}/{len(images)}")

    return images