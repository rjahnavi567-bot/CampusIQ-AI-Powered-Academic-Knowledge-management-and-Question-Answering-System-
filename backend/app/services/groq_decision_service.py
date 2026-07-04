def should_use_groq(image):
    """
    Decide whether Groq Vision should analyze this image.
    """

    # Very reliable metadata -> skip Groq
    if image.get("confidence_score", 0) >= 0.85:
        return False

    # Weak classifier
    if image.get("classification_confidence", 0) < 0.65:
        return True

    # No figure title
    if len(image.get("title", "").strip()) < 6:
        return True

    # Very little OCR
    if len(image.get("ocr_text", "").split()) < 3:
        return True

    # Weak caption
    if len(image.get("caption", "").split()) < 4:
        return True

    return False