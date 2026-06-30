def get_page_text(page_lookup, page_no):
    """
    Returns page text using lookup dictionary.
    """

    return page_lookup.get(page_no, "")