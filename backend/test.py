from app.services.retrieval.hybrid_retrieval_service import hybrid_retrieve
from app.services.retrieval.unified.result_builder import build_results
from app.services.retrieval.unified.result_fusion import fuse_results

# -------------------------------------
# Query
# -------------------------------------

query = "microprogram sequencer"

# -------------------------------------
# Retrieve
# -------------------------------------

documents, metadatas, scores = hybrid_retrieve(
    question=query,
    top_k=20
)

# -------------------------------------
# Build Result Objects
# -------------------------------------

results = build_results(
    documents,
    metadatas,
    scores
)

# -------------------------------------
# Fuse & Rank
# -------------------------------------

results = fuse_results(
    results,
    top_k=10
)

# -------------------------------------
# Display
# -------------------------------------

print("\n========== FINAL RESULTS ==========\n")

for i, item in enumerate(results, start=1):

    print(f"Rank {i}")
    print("Type :", item["metadata"]["retrieval_type"])
    print("Score:", round(item["score"], 3))
    print("Page :", item["metadata"].get("page_no"))
    print(item["document"][:200])
    print("-" * 50)