import cv2

from app.services.image_v2.doclayout_experiment.detector import detect_layout
from app.services.image_v2.doclayout_experiment.visualizer import draw_boxes
from app.services.image_v2.doclayout_experiment.extractor import extract_regions
from app.services.image_v2.doclayout_experiment.evaluator import summarize


IMAGE = "page_156.png"

result = detect_layout(IMAGE)

print(summarize(result))

img = draw_boxes(result)

cv2.imwrite("prediction.png", img)

saved = extract_regions(
    result,
    "output"
)

print("Saved:", len(saved))