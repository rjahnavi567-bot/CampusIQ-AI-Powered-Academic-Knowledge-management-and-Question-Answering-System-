# clear_db.py

import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

client.delete_collection("academic_documents")

print("Collection deleted")