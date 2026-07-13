import re

# --------------------------------------------------
# Common words to ignore
# --------------------------------------------------

STOPWORDS = {

    "the", "a", "an", "is", "are", "was", "were",

    "this", "that", "these", "those",

    "there", "here",

    "of", "on", "in", "into", "to",

    "with", "without", "from", "for",

    "and", "or", "by", "at",

    "has", "have", "had",

    "shows", "showing", "show",

    "image", "picture", "photo",

    "black", "white",

    "it", "its",

    "be"

}


# --------------------------------------------------
# Clean text
# --------------------------------------------------

def tokenize(text):

    text = text.lower()

    words = re.findall(

        r"[a-zA-Z0-9_]+",

        text

    )

    return words


# --------------------------------------------------
# One image
# --------------------------------------------------

def extract_keywords(image):

    caption = getattr(

        image,

        "clean_caption",

        ""

    )

    ocr = getattr(

        image,

        "clean_ocr",

        ""

    )

    combined = caption + " " + ocr

    words = tokenize(combined)

    keywords = []

    seen = set()

    for word in words:

        if len(word) < 3:

            continue

        if word in STOPWORDS:

            continue

        if word.isdigit():

            continue

        if word in seen:

            continue

        seen.add(word)

        keywords.append(word)

    image.keywords = keywords

    return image


# --------------------------------------------------
# Batch
# --------------------------------------------------

def extract_all_keywords(images):

    print("\n==============================")
    print("STAGE 9.4 : KEYWORD EXTRACTOR")
    print("==============================")

    for image in images:

        extract_keywords(image)

    print(f"Keywords Extracted : {len(images)}")

    print("\nSamples\n")

    for image in images[:5]:

        print(f"Page {image.page_no}")

        print(image.keywords)

        print()

    return images