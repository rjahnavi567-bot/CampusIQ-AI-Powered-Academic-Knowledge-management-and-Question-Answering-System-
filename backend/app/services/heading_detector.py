import re

def is_heading(text):

    text = text.strip()

    if len(text) < 80:

        if text.isupper():
            return True

        if text.endswith(":"):
            return True

        if re.match(r"^\d+(\.\d+)*", text):
            return True

    return False