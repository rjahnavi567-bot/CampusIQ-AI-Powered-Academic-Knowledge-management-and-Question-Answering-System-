import re

def clean_text(text):

    if not text:
        return ""

    text = text.replace("\x00", "")

    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', text)

    return text