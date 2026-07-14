import math


# ----------------------------------------
# Convert Chroma Distance → Similarity
# ----------------------------------------

def distance_to_similarity(distance):

    return round(
        1.0 / (1.0 + distance),
        4
    )


# ----------------------------------------
# Normalize Score List
# ----------------------------------------

def normalize_scores(scores):

    print("\n==============================")
    print("STAGE 12.2 : SCORE NORMALIZER")
    print("==============================")

    normalized = []

    for score in scores:

        normalized.append(

            distance_to_similarity(score)

        )

    print(f"Normalized : {len(normalized)}")

    print("\nSamples\n")

    for raw, sim in zip(scores[:5], normalized[:5]):

        print(

            f"Distance={raw:.3f} | Similarity={sim:.3f}"

        )

    return normalized