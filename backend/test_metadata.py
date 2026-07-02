from app.services.chroma_service import text_collection

results = text_collection.get(
    include=["metadatas"]
)

files = set()

for meta in results["metadatas"]:
    files.add(meta["source_file"])

print("\nFILES INSIDE CHROMADB\n")

for f in sorted(files):
    print(f)