from app.services.chroma_service import collection

data = collection.get()

print("Number of documents:", len(data["documents"]))

for i in range(min(5, len(data["documents"]))):
    print("\nDOCUMENT:", i)
    print(data["documents"][i][:300])