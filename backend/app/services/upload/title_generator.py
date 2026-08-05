import os

from app.services.metadata_service import extract_metadata
from app.services.title_service import generate_title


def generate_document_title(
    file_path,
    pages,
    preview_text,
    original_filename,
    subject_result=None
):
    """
    Generates a smart filename for uploaded document.
    """

    metadata = extract_metadata(file_path)

    suggested_title = generate_title(metadata)

####################################################
# Fallback title from document content
####################################################

    if suggested_title == "Untitled_Document":

        words = []

        for word in preview_text.split():

            word = word.strip()

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

####################################################
# Prefix detected subject
####################################################

    if subject_result:

        subject = subject_result.get("primary_subject")

        if subject:

            subject = subject.replace("/", "_").replace(" ", "_")

            if not suggested_title.lower().startswith(subject.lower()):

               suggested_title = f"{subject}_{suggested_title}"
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