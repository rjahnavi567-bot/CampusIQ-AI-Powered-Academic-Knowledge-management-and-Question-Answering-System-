import re
from app.services.keyword_service import extract_keywords
def create_semantic_chunks(text):

    chunks = []

    # Split by empty lines (paragraphs)
    paragraphs = re.split(r'\n\s*\n', text)

    for para in paragraphs:

        para = para.strip()

        if len(para) < 50:
            continue

        # First sentence becomes topic
        first_sentence = para.split('.')[0].strip()

        topic = first_sentence[:100]
        print("Keywords:", extract_keywords(para))
        chunks.append({
    "topic": topic,
    "content": para,
    "keywords": extract_keywords(para)
})
        

    return chunks