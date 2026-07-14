from sqlalchemy.orm import Session

from app.database.connection import SessionLocal

from app.services.image_v2.embedding_generator import get_embedding_model

from app.services.retrieval.unified.unified_retriever import (
    unified_retrieve
)
from app.services.retrieval.unified.unified_ranker import unified_rank
query = "microprogram sequencer"

db: Session = SessionLocal()

model = get_embedding_model()

query_embedding = model.encode(
    query,
    normalize_embeddings=True
).tolist()

results = unified_retrieve(
    db=db,
    query=query,
    query_embedding=query_embedding
)


results = unified_rank(results)

print()

print("=" * 60)

for i, r in enumerate(results[:10], start=1):

    print()

    print(f"Rank {i}")

    print("Source :", r["source"])

    if r["source"] == "image":

        print(r["id"])

        print(r["document"][:200])

    else:

        print(r)