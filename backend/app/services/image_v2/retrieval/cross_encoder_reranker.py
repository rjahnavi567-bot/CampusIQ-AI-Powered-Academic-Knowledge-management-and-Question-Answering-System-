from sentence_transformers import CrossEncoder

# --------------------------------------------------
# Singleton Model
# --------------------------------------------------

_model = None


def get_model():

    global _model

    if _model is None:

        print("Loading Cross Encoder...")

        _model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    return _model


# --------------------------------------------------
# Re-rank Results
# --------------------------------------------------

def rerank(query, results):

    print("\n==============================")
    print("STAGE 11.2 : CROSS ENCODER")
    print("==============================")

    if len(results) == 0:
        return results

    model = get_model()

    pairs = []

    for result in results:

        pairs.append(

            (
                query,
                result["document"]
            )

        )

    scores = model.predict(pairs)

    for result, score in zip(results, scores):

        result["cross_score"] = float(score)

    results.sort(

        key=lambda x: x["cross_score"],

        reverse=True

    )

    print(f"Re-ranked : {len(results)}")

    print("\nTop Results\n")

    for r in results[:5]:

        print(

            f"{r['id']}"

            f" | Cross={r['cross_score']:.3f}"

            f" | Hybrid={r['score']:.3f}"

        )

    return results