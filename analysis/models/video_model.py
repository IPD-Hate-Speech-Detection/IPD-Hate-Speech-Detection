from gradio_client import Client, handle_file # type: ignore
from typing import List, Dict, Union, Tuple
import os
from config.config import MODEL_URLS

class VideoModel:
    def __init__(self):
        self.client = Client(MODEL_URLS["video"])
    
    def predict(self, video_path: str) -> Dict:
        if video_path.startswith(('http://', 'https://')):
            video = handle_file(video_path)
        else:
            video = video_path
            
        result = self.client.predict({"video": video}, api_name="/predict")
        return result
    
    def predict_batch(self, video_paths: List[str]) -> List[Dict]:
        results = []
        for path in video_paths:
            results.append(self.predict(path))
        return results
