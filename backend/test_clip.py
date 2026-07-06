import os

from app.services.image_v2.clip_service import embed_image

folder = "layout_output"

files = sorted(os.listdir(folder))

path = os.path.join(

    folder,

    files[0]

)

embedding = embed_image(path)

print(len(embedding))

print()

print(embedding[:20])