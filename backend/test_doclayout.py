from ultralytics import YOLO

model = YOLO(
    "models/doclayout/doclayout_yolo_docstructbench_imgsz1024.pt"
)

print("Model loaded successfully!")

print(model.names)