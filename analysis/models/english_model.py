from gradio_client import Client # type: ignore
from typing import List, Tuple
from config.config import MODEL_URLS

class EnglishTextModel:
    def __init__(self):
        self.client = Client(MODEL_URLS["english_text"])
    
    def predict(self, text: str) -> Tuple[str, float]:
        result = self.client.predict(text, api_name="/predict")
        return result  # Already returns (label, confidence)
    
    def predict_batch(self, texts: List[str]) -> List[Tuple[str, float]]:
        results = []
        for text in texts:
            results.append(self.predict(text))
        return results
