import torch
from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
import gradio as gr

model = ViTForImageClassification.from_pretrained('Tirath5504/IPD-Image-ViT-Finetune')
processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')

class_names = ['cut_throat_gesture', 'finger_gun_to_the_head', 'middle_finger', 'slanted_eyes_gesture', 'swastika']

def predict(image):
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs).logits

    predicted_class_idx = outputs.argmax(-1).item()
    predicted_class = class_names[predicted_class_idx]

    return predicted_class

iface = gr.Interface(fn=predict,
                     inputs=gr.Image(type="pil"),
                     outputs=gr.Label(num_top_classes=1),
                     title="Hateful Content Detection",
                     description="Upload an image to classify hateful gestures or symbols")

iface.launch(debug=True, share=True)