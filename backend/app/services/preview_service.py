def build_preview_text(
    pages,
    max_pages=5,
    max_chars=8000
):
    """
    Builds a preview text used by

    - Subject Detection
    - Title Generation
    - Future Unit Detection
    - Future Groq Classification

    Returns one cleaned string.
    """

    preview = ""

    for page in pages[:max_pages]:

        text = page["text"].strip()

        preview += text + "\n"

        if len(preview) >= max_chars:
            break

    return preview[:max_chars]