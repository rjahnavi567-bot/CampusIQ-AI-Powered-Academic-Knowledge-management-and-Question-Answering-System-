import os

from app.services.metadata_service import extract_metadata
from app.services.title_service import generate_title


def generate_document_title(file_path, pages, original_filename):
    """
    Generates a smart filename for uploaded document.
    """

    metadata = extract_metadata(file_path)

    suggested_title = generate_title(metadata)

    if suggested_title == "Untitled_Document":

        full_text = ""

        for page in pages:
            full_text += page["text"][:1000] + " "

        words = []

        for word in full_text.split():

            if len(word) > 3:
                words.append(word)

            if len(words) >= 8:
                break

        if words:
            suggested_title = "_".join(words)

        else:
            suggested_title = os.path.splitext(
                original_filename
            )[0]

    suggested_title = (
        suggested_title
        .replace(":", "")
        .replace(",", "")
        .replace(".", "")
        .replace("/", "_")
        .replace("\\", "_")
        .replace("?", "")
        .replace("*", "")
        .replace('"', "")
        .replace("<", "")
        .replace(">", "")
        .replace("|", "")
    )

    suggested_title = suggested_title[:100]

    extension = os.path.splitext(
        original_filename
    )[1]

    new_filename = suggested_title + extension

    counter = 1

    while os.path.exists(f"uploads/{new_filename}"):

        new_filename = (
            f"{suggested_title}"
            f"_v{counter}"
            f"{extension}"
        )

        counter += 1

    new_file_path = f"uploads/{new_filename}"

    return suggested_title, new_filename, new_file_path