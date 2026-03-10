from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.train(
    data="/home/gmurthy/Pictures/badges/badge-data.yaml",
    epochs=100,
    imgsz=640,
    name="badge-demo",
)
