from gradio_client import Client, handle_file # type: ignore
from typing import List, Dict
import os
from config.config import MODEL_URLS

class ImageModel:
    def __init__(self):
        self.client = Client(MODEL_URLS["image"])
    
    def predict(self, image_path: str) -> Dict:
        # if image_path.startswith(('http://', 'https://')):
        #     image = handle_file(image_path)
        # else:
        #     image = image_path

        image = handle_file(image_path)
            
        result = self.client.predict(image, api_name="/predict")
        return result
    
    def predict_batch(self, image_paths: List[str]) -> List[Dict]:
        results = []
        for path in image_paths:
            results.append(self.predict(path))
        return results
