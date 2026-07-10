import torch
import torch.nn.functional as F


# --------------------------------------------------
# Similarity Classification
# --------------------------------------------------

def classify_images(images, prompt_embeddings):

    print("\n==============================")
    print("SIMILARITY CLASSIFIER")
    print("==============================")

    for image in images:

        if not image.clip_embedding:
            continue

        image_vector = torch.tensor(
            image.clip_embedding,
            dtype=torch.float32
        )

        scores = {}

        best_category = ""
        best_score = -1.0

        for category, embeddings in prompt_embeddings.items():

            similarities = F.cosine_similarity(

        image_vector.unsqueeze(0),

        embeddings,

        dim=1

    )

            category_score = similarities.max().item()

            scores[category] = round(category_score, 4)

            if category_score > best_score:

                best_score = category_score
                best_category = category

        image.vision_scores = scores

        image.vision_class = best_category

        image.vision_confidence = round(best_score, 4)
    print(f"Vision classified : {len(images)}")

    print("\n==============================")
    print("TOP CATEGORY SCORES")
    print("==============================")

    for image in images[:5]:

        print(f"\nPage {image.page_no}")
        print(f"Image : {image.path}")

        ranked = sorted(
        image.vision_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

        for category, score in ranked:

            print(f"{category:15} {score:.3f}")

    return images