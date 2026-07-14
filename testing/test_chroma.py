from app.services.chroma_service import collection

results = collection.query(
    query_texts=["Gathering took place at?"],
    n_results=1
)

print(results)