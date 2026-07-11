# --------------------------------------------------
# OCR Scorer
# --------------------------------------------------

GOOD_WORDS = 20

MAX_WORDS = 300

GOOD_TEXT_AREA = 0.10

MAX_TEXT_AREA = 0.60


# --------------------------------------------------
# Word Count Score
# --------------------------------------------------

def score_word_count(image):

    words = image.word_count

    # diagrams/photos usually have few words
    if words <= GOOD_WORDS:
        return 1.0

    # text page
    if words >= MAX_WORDS:
        return 0.0

    return 1.0 - (

        (words - GOOD_WORDS)

        /

        (MAX_WORDS - GOOD_WORDS)

    )


# --------------------------------------------------
# Text Area Score
# --------------------------------------------------

def score_text_area(image):

    ratio = image.text_area_ratio

    if ratio <= GOOD_TEXT_AREA:
        return 1.0

    if ratio >= MAX_TEXT_AREA:
        return 0.0

    return 1.0 - (

        (ratio - GOOD_TEXT_AREA)

        /

        (MAX_TEXT_AREA - GOOD_TEXT_AREA)

    )


# --------------------------------------------------
# Paragraph Score
# --------------------------------------------------

def score_paragraph(image):

    if image.has_paragraph:
        return 0.0

    return 1.0


# --------------------------------------------------
# Heading Score
# --------------------------------------------------

def score_heading(image):

    if image.has_heading:
        return 0.5

    return 1.0


# --------------------------------------------------
# Bullet Score
# --------------------------------------------------

def score_bullets(image):

    if image.bullet_count == 0:
        return 1.0

    if image.bullet_count >= 10:
        return 0.0

    return 1 - (image.bullet_count / 10)


# --------------------------------------------------
# Final OCR Score
# --------------------------------------------------

def compute_ocr_score(image):
    if image.hard_reject:

        image.ocr_score = 0.0

        return image

    word = score_word_count(image)

    area = score_text_area(image)

    paragraph = score_paragraph(image)

    heading = score_heading(image)

    bullets = score_bullets(image)

    image.ocr_score = round(

        (

            word +

            area +

            paragraph +

            heading +

            bullets

        ) / 5,

        3

    )

    return image


# --------------------------------------------------
# Batch
# --------------------------------------------------

def score_ocr(images):

    print("\n==============================")
    print("OCR SCORER")
    print("==============================")

    for image in images:

        compute_ocr_score(image)

    print(f"OCR scored : {len(images)}")

    print("\nSample Scores")

    for image in images[:5]:

        print(

            f"Page {image.page_no} | "

            f"OCR Score = {image.ocr_score:.3f}"

        )

    return images