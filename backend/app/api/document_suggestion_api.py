from fastapi import APIRouter
from app.services.document_cache import document_cache

router = APIRouter(tags=["Documents"])


@router.get("/documents/suggestions")
def suggestions(query: str):

    query = query.lower()

    results = []

    for filename in document_cache.keys():

        if query in filename.lower():

            results.append(filename)

        if len(results) == 8:
            break

    return results