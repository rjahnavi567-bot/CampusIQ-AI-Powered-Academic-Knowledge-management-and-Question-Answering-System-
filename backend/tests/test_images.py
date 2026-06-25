from app.services.chroma_service import collection

results = collection.get()

for doc, meta in zip(
    results["documents"],
    results["metadatas"]
):

    if meta.get("type") == "image":

        print("\nIMAGE FOUND")
        print(meta)
        print(doc[:300])