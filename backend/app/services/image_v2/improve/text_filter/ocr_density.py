import cv2
import pytesseract


# -------------------------------
# Configuration
# -------------------------------

MAX_WORDS = 120

MAX_CHARACTERS = 900

MIN_TEXT_RATIO = 0.70


def compute_text_density(image):
    """
    Computes OCR statistics.

    Returns
    -------
    {
        word_count,
        char_count,
        text_ratio
    }
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(
        gray,
        output_type=pytesseract.Output.DICT
    )

    words = []

    total_text_area = 0

    image_area = image.shape[0] * image.shape[1]

    n = len(data["text"])

    for i in range(n):

        text = data["text"][i].strip()

        if text == "":
            continue

        words.append(text)

        w = data["width"][i]

        h = data["height"][i]

        total_text_area += w * h

    word_count = len(words)

    char_count = sum(len(w) for w in words)

    text_ratio = total_text_area / image_area

    return {

        "word_count": word_count,

        "char_count": char_count,

        "text_ratio": text_ratio

    }


def is_text_heavy(image):
    """
    Decide whether this crop is mostly text.
    """

    stats = compute_text_density(image)

    reject = False

    if stats["word_count"] > MAX_WORDS:
        reject = True

    if stats["char_count"] > MAX_CHARACTERS:
        reject = True

    if stats["text_ratio"] > MIN_TEXT_RATIO:
        reject = True

    stats["reject"] = reject

    return stats