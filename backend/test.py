from app.services.image_v2.duplicate_filter import remove_duplicates
import os

images = []

folder = "layout_output"

for file in os.listdir(folder):

    images.append({
        "path": os.path.join(folder, file)
    })

filtered = remove_duplicates(images)

print("Original :", len(images))
print("After duplicate removal :", len(filtered))