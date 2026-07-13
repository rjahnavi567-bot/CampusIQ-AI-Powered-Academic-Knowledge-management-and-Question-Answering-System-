from typing import List


def build_context(image, page_chunks: List[str]):

    """
    Build surrounding context for one image.
    """

    context = {

        "page_title": "",

        "section_heading": "",

        "figure_caption": "",

        "previous_text": "",

        "next_text": "",

        "nearby_text": ""

    }

    if not page_chunks:

        image.context = context
        image.page_context = ""

        return image

    # ----------------------------------------
    # Simple Version
    # ----------------------------------------

    context["previous_text"] = page_chunks[0]

    if len(page_chunks) > 1:
        context["next_text"] = page_chunks[1]

    context["nearby_text"] = "\n".join(page_chunks[:3])

    image.context = context

    image.page_context = context["nearby_text"]

    return image