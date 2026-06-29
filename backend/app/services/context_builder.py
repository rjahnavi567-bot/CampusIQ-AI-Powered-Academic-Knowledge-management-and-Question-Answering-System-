def build_context(results):

    context = ""

    for result in results:

        content = result["content"]
        meta = result["metadata"]

        page = meta.get("page_no", "")
        source = meta.get("source_file", "")

        if meta.get("type") == "image":

            context += (
                "\n"
                "================ IMAGE =================\n"
                f"Page: {page}\n"
                f"Source: {source}\n\n"
                f"{content}\n"
                "========================================\n\n"
            )

        else:

            context += (
                "\n"
                "================ TEXT ==================\n"
                f"Page: {page}\n"
                f"Source: {source}\n\n"
                f"{content}\n"
                "========================================\n\n"
            )

    return context