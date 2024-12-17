from ultralytics import YOLO
from transformers import CLIPProcessor, CLIPModel


def load_models():
    model = YOLO("yolov8x-seg.pt")
    clip_model = CLIPModel.from_pretrained("clip-vit-base-patch32")
    clip_processor = CLIPProcessor.from_pretrained("clip-vit-base-patch32")
    return model, clip_model, clip_processor
