def build_context(results):

    context = ""

    for result in results:

        content = result.get(
            "content",
            ""
        )

        metadata = result.get(
            "metadata",
            {}
        )

        source_file = metadata.get(
            "source_file",
            "Unknown"
        )

        page_no = metadata.get(
            "page_no",
            "Unknown"
        )

        similarity = metadata.get(
            "similarity_score",
            result.get("score", 0)
        )

        context += (
            f"{content}\n\n"
            f"Source: {source_file}\n"
            f"Page: {page_no}\n"
            f"Similarity: {similarity}\n\n"
        )

    return context