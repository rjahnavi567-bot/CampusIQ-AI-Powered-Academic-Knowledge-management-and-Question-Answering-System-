import re

def generate_title(metadata):

    title = metadata.get(
        "title",
        ""
    ).strip()

    subject = metadata.get(
        "subject",
        ""
    ).strip()

    if title:

        return clean_title(title)

    if subject:

        return clean_title(subject)

    return "Untitled_Document"


def clean_title(text):

    text = re.sub(
        r'[\\/*?:"<>|]',
        "",
        text
    )

    text = text.replace(
        " ",
        "_"
    )

    return text[:100]