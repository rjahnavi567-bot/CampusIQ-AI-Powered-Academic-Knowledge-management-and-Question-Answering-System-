from fastapi import APIRouter
from app.services.chroma_service import collection
from urllib.parse import quote
router = APIRouter()


@router.get("/search-documents")
def search_documents(query: str):

    results = collection.query(
        query_texts=[query],
        n_results=20
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    response = []

    for doc, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        score = round(
    100 * (
        1 / (1 + distance)
    )
)

        if score < 35:
            score = score + 20

        score = min(score, 100)

        response.append(
    {
        "file":
        metadata.get(
            "source_file"
        ),

        "page":
        metadata.get(
            "page_no"
        ),

        "score":
        score,

        "text":
doc[:500],

"full_text":
doc,

        "url":
        f"http://localhost:8000/uploads/"
        f"{quote(metadata.get('source_file'))}"
        f"#page={metadata.get('page_no')}"
    }
)
    return response