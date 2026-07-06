import os

from app.services.image_v2.embedding_pipeline import generate_embeddings

folder = "layout_output"

images = []

for file in sorted(os.listdir(folder))[:5]:

    images.append({

        "path": os.path.join(folder,file)

    })

images = generate_embeddings(images)

for img in images:

    print(

        len(img["clip_embedding"])

    )