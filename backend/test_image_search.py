from app.services.image_v2.image_retriever import search_images

results = search_images(
    "data integration diagram"
)

for r in results:

    print()

    print("Score:", r.score)

    print(r.payload)