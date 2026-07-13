import re


# -----------------------------------------
# Remove Florence padding tokens
# -----------------------------------------

def remove_padding(text: str) -> str:

    text = re.sub(r"<pad>", "", text, flags=re.IGNORECASE)

    return text


# -----------------------------------------
# Remove duplicate spaces
# -----------------------------------------

def normalize_spaces(text: str) -> str:

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -----------------------------------------
# Remove repeated punctuation
# -----------------------------------------

def normalize_punctuation(text: str) -> str:

    text = re.sub(r"\.{2,}", ".", text)

    text = re.sub(r",{2,}", ",", text)

    return text


# -----------------------------------------
# Remove meaningless Florence phrases
# -----------------------------------------

BAD_PHRASES = [

    "the image appears to be",

    "this image appears to be",

    "there is",

    "there are",

]


def remove_bad_phrases(text: str) -> str:

    lower = text.lower()

    for phrase in BAD_PHRASES:

        lower = lower.replace(phrase, "")

    return lower


# -----------------------------------------
# Capitalize first letter
# -----------------------------------------

def normalize_case(text: str) -> str:

    if len(text) == 0:

        return text

    return text[0].upper() + text[1:]


# -----------------------------------------
# Clean one caption
# -----------------------------------------

def clean_caption(image):

    caption = image.florence_caption or ""

    caption = remove_padding(caption)

    caption = normalize_punctuation(caption)

    caption = remove_bad_phrases(caption)

    caption = normalize_spaces(caption)

    caption = normalize_case(caption)

    image.cleaned_caption = caption

    return image


# -----------------------------------------
# Batch Processing
# -----------------------------------------

def clean_captions(images):

    print("\n==============================")
    print("STAGE 9.1 : CAPTION CLEANER")
    print("==============================")

    for image in images:

        clean_caption(image)

    print(f"Cleaned : {len(images)}")

    print("\nSamples\n")

    for image in images[:5]:

        print(f"Page {image.page_no}")

        print("Original :")

        print(image.florence_caption)

        print()

        print("Cleaned :")

        print(image.cleaned_caption)

        print()

    return images