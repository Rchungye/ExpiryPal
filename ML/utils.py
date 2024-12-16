import cv2
import os
import torch

def enhance_contrast(img, alpha=3.0, beta=30):
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def extract_features(image, clip_model, clip_processor):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    inputs = clip_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        features = clip_model.get_image_features(**inputs)
    return features.cpu().numpy().flatten()

def extract_items(image_path, output_folder, model, clip_model, clip_processor):
    img = cv2.imread(image_path)
    img_contrast = enhance_contrast(img)
    results = model(img_contrast)
    os.makedirs(output_folder, exist_ok=True)

    items = []
    for i, box in enumerate(results[0].boxes):
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        class_id = int(box.cls)
        class_name = results[0].names[class_id]

        cropped_img = img[y1:y2, x1:x2]
        output_path = os.path.join(output_folder, f"{class_name}_{i+1}.jpg")
        cv2.imwrite(output_path, cropped_img)

        features = extract_features(cropped_img, clip_model, clip_processor)
        items.append({'name': class_name, 'features': features, 'cropped_img': output_path})

    return items
