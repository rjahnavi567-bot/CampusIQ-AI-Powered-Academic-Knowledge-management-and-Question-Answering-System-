def create_content_signature(pages):

    full_text = ""

    for page in pages:

        full_text += page["text"] + "\n"

    words = full_text.split()

    first_part = " ".join(words[:2000])

    last_part = " ".join(words[-2000:])

    return first_part + "\n" + last_part