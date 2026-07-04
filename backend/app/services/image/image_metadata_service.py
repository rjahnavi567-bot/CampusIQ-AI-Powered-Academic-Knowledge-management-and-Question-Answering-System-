import os

from app.services.figure_title_service import extract_figure_title
from app.services.diagram_title_service import generate_diagram_title
from app.services.image_context_service import get_page_text


def build_metadata(image, page_lookup):

    page_text = get_page_text(
        page_lookup,
        image["page_no"]
    )

    image["page_text"] = page_text

    title, confidence = extract_figure_title(
        page_text
    )

    if title:

        image["title"] = title

    else:

        image["title"] = generate_diagram_title(
            image["caption"],
            image["ocr_text"]
        )

    return image