from .context_builder import build_context


def build_contexts(images, page_text_lookup):

    print("\n==============================")
    print("STAGE 11.3 : CONTEXT EXPANSION")
    print("==============================")

    for image in images:

        page_chunks = page_text_lookup.get(
            image.page_no,
            []
        )

        build_context(
            image,
            page_chunks
        )

    print(f"Contexts Built : {len(images)}")

    print("\nSamples\n")

    for image in images[:5]:

        print(f"Page {image.page_no}")

        print(image.page_context[:300])

        print()

    return images