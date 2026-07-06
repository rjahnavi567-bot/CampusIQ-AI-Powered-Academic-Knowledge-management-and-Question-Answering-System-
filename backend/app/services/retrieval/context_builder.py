def build_context(results):

    context = ""

    context += "===== TEXT =====\n\n"

    for chunk in results["text"]:

        context += chunk.payload["text"]

        context += "\n\n"

    context += "===== IMAGES =====\n\n"

    for image in results["images"]:

        payload = image.payload

        context += f"Caption : {payload.get('caption', '')}\n"
        context += f"OCR : {payload.get('ocr_text', '')}\n"
        context += f"Page : {payload.get('page_no', '')}\n"
        context += "\n"

    return context