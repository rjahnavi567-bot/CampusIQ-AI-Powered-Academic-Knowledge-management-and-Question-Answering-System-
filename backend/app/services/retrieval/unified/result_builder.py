def build_results(
    documents,
    metadatas,
    scores
):

    results = []

    for doc, meta, score in zip(

        documents,

        metadatas,

        scores

    ):

        results.append(

            {

                "document": doc,

                "metadata": meta,

                "score": score

            }

        )

    return results