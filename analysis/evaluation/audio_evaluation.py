from typing import Dict
from tqdm import tqdm # type: ignore
import pandas as pd # type: ignore
from models.audio_model import AudioModel
from utils.metrics import calculate_binary_metrics, save_metrics
from utils.data_loader import load_media_data

def evaluate_audio_model(test_data_path: str = "audio_test_data.csv") -> Dict:
    print("Evaluating Audio Model...")
    
    audio_paths, true_labels = load_media_data(test_data_path)
    
    model = AudioModel()
    
    predictions = []
    scores = []
    languages = []
    
    for audio_path in tqdm(audio_paths, desc="Processing audio files"):
        try:
            result = model.predict(audio_path)
            
            # Extract prediction and confidence
            predictions.append(result["prediction"])
            scores.append(result["confidence"])
            
            # Track language detection
            if result["language"] is not None:
                languages.append(result["language"])
                
        except Exception as e:
            print(f"Error processing {audio_path}: {e}")
            predictions.append("not_hate")  # Default to safe prediction on error
            scores.append(0.0)
    
    binary_metrics = calculate_binary_metrics(true_labels, predictions, scores)
    
    language_distribution = pd.Series(languages).value_counts().to_dict() if languages else {}
    
    metrics = {
        "binary_classification": binary_metrics,
        "language_distribution": language_distribution
    }
    
    save_metrics(metrics, "audio")
    
    print(f"Audio Model Evaluation Complete - F1 Score: {binary_metrics['f1_score']:.4f}")
    
    return metrics
