from app.services.image_v2.embedding_generator import generate_query_embedding
from app.services.image_v2.retrieval.hybrid_retriever import hybrid_search
from app.services.image_v2.retrieval.cross_encoder_reranker import rerank
query = "microprogram sequencer for a control memory"

print("\n==============================")
print("STAGE 11 : HYBRID RETRIEVAL")
print("==============================")
print("Query:", query)

query_embedding = generate_query_embedding(query)

results = hybrid_search(
    query=query,
    embedding=query_embedding,
    top_k=20
)


results = rerank(query, results)

for i, r in enumerate(results[:10], start=1):

    print("\n---------------------------------------")
    print(f"Rank {i}")
    print("ID       :", r["id"])
    print("Hybrid   :", round(r["score"], 3))
    print("Semantic :", round(r["semantic"], 3))
    print("Keyword  :", round(r["keyword"], 3))

    print("\nDocument:")
    print(r["document"][:300])