from app.services.retrieval.image.clip_image_search import retrieve_clip_images

results = retrieve_clip_images(
    question="Explain the pipeline diagram",
    top_k=5
)

print()

print("Returned:", len(results))

for r in results:

    print(r["metadata"]["page_no"], r["score"])