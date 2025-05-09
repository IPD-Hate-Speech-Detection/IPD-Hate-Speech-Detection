from gradio_client import Client, handle_file # type: ignore
from typing import List, Dict, Union, Tuple
import os
from config.config import MODEL_URLS

class AudioModel:
    def __init__(self):
        self.client = Client(MODEL_URLS["audio"])
    
    def predict(self, audio_path: str) -> Dict:
        # if audio_path.startswith(('http://', 'https://')):
        #     audio = handle_file(audio_path)
        # else:
        #     audio = audio_path
        audio = handle_file(audio_path)
        result = self.client.predict(audio, api_name="/predict")
        return result
    
    def predict_batch(self, audio_paths: List[str]) -> List[Dict]:
        results = []
        for path in audio_paths:
            results.append(self.predict(path))
        return results
