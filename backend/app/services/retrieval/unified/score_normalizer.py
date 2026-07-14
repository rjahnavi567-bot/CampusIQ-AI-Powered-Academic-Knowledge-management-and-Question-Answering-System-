import math


# ----------------------------------------
# Convert Chroma distance -> similarity
# ----------------------------------------

def distance_to_similarity(distance):

    return 1.0 / (1.0 + distance)


# ----------------------------------------
# Normalize one retrieval result
# ----------------------------------------

def normalize_result(result):

    score = result.get("score", 1.0)

    similarity = distance_to_similarity(score)

    result["raw_distance"] = score

    result["normalized_score"] = round(similarity, 4)

    return result


# ----------------------------------------
# Normalize all retrieval results
# ----------------------------------------

def normalize_scores(results):

    print("\n==============================")
    print("STAGE 12.2 : SCORE NORMALIZER")
    print("==============================")

    normalized = []

    for result in results:

        normalized.append(

            normalize_result(result)

        )

    print(f"Normalized : {len(normalized)}")

    print("\nSamples\n")

    for item in normalized[:5]:

        print(

            f'{item["retrieval_type"]:5} | '

            f'Distance={item["raw_distance"]:.3f} | '

            f'Normalized={item["normalized_score"]:.3f}'

        )

    return normalized