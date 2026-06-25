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

        chunk_type = metadata.get(
            "type",
            "text"
        )

        if chunk_type == "image":

            context += (

                "\n========== IMAGE ==========\n"

                f"{content}\n\n"

                f"Source File: {source_file}\n"

                f"Page: {page_no}\n\n"

            )

        else:

            context += (

                "\n========== TEXT ==========\n"

                f"{content}\n\n"

                f"Source File: {source_file}\n"

                f"Page: {page_no}\n\n"

            )

    return context