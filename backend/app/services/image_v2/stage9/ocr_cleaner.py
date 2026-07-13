import re


# -----------------------------------------
# Remove repeated whitespace
# -----------------------------------------

def normalize_spaces(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -----------------------------------------
# Remove repeated punctuation
# -----------------------------------------

def remove_noise(text):

    # remove long underscore groups
    text = re.sub(r"_+", " ", text)

    # remove repeated dots
    text = re.sub(r"\.{2,}", " ", text)

    # remove repeated dashes
    text = re.sub(r"-{3,}", " ", text)

    # remove repeated equal signs
    text = re.sub(r"={2,}", " ", text)

    # remove repeated pipes
    text = re.sub(r"\|{2,}", " ", text)

    return text


# -----------------------------------------
# Remove isolated symbols
# -----------------------------------------

def remove_symbols(text):

    text = re.sub(r"[^\w\s\.,:/()%+-]", " ", text)

    return text


# -----------------------------------------
# Clean one OCR
# -----------------------------------------

def clean_ocr(image):

    text = getattr(image, "ocr_text", "")

    if text is None:
        text = ""

    text = remove_noise(text)

    text = remove_symbols(text)

    text = normalize_spaces(text)

    image.cleaned_ocr = text

    return image


# -----------------------------------------
# Batch
# -----------------------------------------

def clean_ocrs(images):

    print("\n==============================")
    print("STAGE 9.2 : OCR CLEANER")
    print("==============================")

    for image in images:

        clean_ocr(image)

    print(f"Cleaned : {len(images)}")

    print("\nSamples\n")

    for image in images[:5]:

        print(f"Page {image.page_no}")

        print("Original OCR:")

        print(getattr(image, "ocr_text", ""))

        print()

        print("Cleaned OCR:")

        print(image.cleaned_ocr)

        print()

    return images