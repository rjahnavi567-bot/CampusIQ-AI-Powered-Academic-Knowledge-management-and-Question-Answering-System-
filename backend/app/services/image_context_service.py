def get_page_text(page_no, pages):
    """
    Returns the full text of the page
    where the image was extracted.
    """

    for page in pages:

        if page["page_no"] == page_no:

            return page["text"]

    return ""