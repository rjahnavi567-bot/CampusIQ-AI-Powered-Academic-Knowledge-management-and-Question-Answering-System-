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

        best_prompt = ""
        best_score = -1.0

        ##################################################
        # Compare against every prompt
        ##################################################

        for prompt, prompt_vector in prompt_embeddings.items():

            similarity = F.cosine_similarity(
                image_vector.unsqueeze(0),
                prompt_vector.unsqueeze(0)
            ).item()

            scores[prompt] = round(similarity, 4)

            if similarity > best_score:

                best_score = similarity
                best_prompt = prompt

        ##################################################
        # Save results
        ##################################################

        image.vision_scores = scores

        image.vision_class = best_prompt

        image.vision_confidence = round(
            best_score,
            4
        )

    print(f"Vision classified : {len(images)}")

    print("\nSample Predictions\n")

    for image in images[:5]:

        print(

            f"Page {image.page_no} | "

            f"{image.vision_class:20}"

            f"{image.vision_confidence:.3f}"

        )

    return images