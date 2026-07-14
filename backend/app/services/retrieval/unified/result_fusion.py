# ----------------------------------------
# Stage 12.3
# Result Fusion & Ranking
# ----------------------------------------

def fuse_results(
    results,
    top_k=10
):

    print("\n==============================")
    print("STAGE 12.3 : RESULT FUSION")
    print("==============================")

    # ------------------------------------
    # Highest score first
    # ------------------------------------

    results.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    # ------------------------------------
    # Remove duplicates
    # ------------------------------------

    fused = []

    seen = set()

    for result in results:

        document = result["document"]

        if document in seen:

            continue

        fused.append(result)

        seen.add(document)

    # ------------------------------------
    # Top K
    # ------------------------------------

    fused = fused[:top_k]

    print("Final Results :", len(fused))

    print("\nTop Results\n")

    for i, item in enumerate(fused[:5], start=1):

        print(

            f"{i}. "

            f'{item["metadata"].get("retrieval_type","text")} '

            f'Score={item["score"]:.3f}'

        )

    return fused