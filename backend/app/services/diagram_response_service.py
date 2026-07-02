def extract_relevant_images(ranked_chunks, max_images=3):
    """
    Returns the best retrieved images that should accompany the answer.
    """

    images = []

    seen = set()

    for chunk in ranked_chunks:

        metadata = chunk["metadata"]

        if metadata.get("type") != "image":
            continue

        image_path = metadata.get("image_path")

        if not image_path:
            continue

        if image_path in seen:
            continue

        seen.add(image_path)

        images.append(
            {
                "image_path": image_path,
                "caption": metadata.get("caption", ""),
                "page_no": metadata.get("page_no"),
                "source_file": metadata.get("source_file")
            }
        )

        if len(images) >= max_images:
            break

    return images