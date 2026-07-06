from app.services.text_rag.retriever import search_text
from app.services.image_v2.image_retriever import search_images


def retrieve_context(question):

    text_results = search_text(
        question,
        limit=5
    )

    image_results = search_images(
        question,
        limit=3
    )

    return {
        "text": text_results,
        "images": image_results
    }