from typing import Dict
from tqdm import tqdm # type: ignore
import pandas as pd # type: ignore
from models.video_model import VideoModel
from utils.metrics import calculate_binary_metrics, save_metrics
from utils.data_loader import load_media_data

def evaluate_video_model(test_data_path: str = "video_test_data.csv") -> Dict:
    print("Evaluating Video Model...")
    
    video_paths, true_labels = load_media_data(test_data_path)
    
    model = VideoModel()
    
    predictions = []
    scores = []
    video_languages = []
    audio_languages = []
    hate_components = []
    
    for video_path in tqdm(video_paths, desc="Processing videos"):
        try:
            result = model.predict(video_path)
            
            # Extract primary prediction and confidence
            predictions.append(result["prediction"])
            scores.append(result["confidence"])
            
            # Track additional metadata
            if "language" in result and result["language"].get("video"):
                video_languages.append(result["language"]["video"])
            
            if "language" in result and result["language"].get("audio"):
                audio_languages.append(result["language"]["audio"])
                
            if "hate_component" in result:
                hate_components.extend(result["hate_component"])
                
        except Exception as e:
            print(f"Error processing {video_path}: {e}")
            predictions.append("not_hate")  # Default to safe prediction on error
            scores.append(0.0)
    
    binary_metrics = calculate_binary_metrics(true_labels, predictions, scores)
    
    video_language_distribution = pd.Series(video_languages).value_counts().to_dict() if video_languages else {}
    audio_language_distribution = pd.Series(audio_languages).value_counts().to_dict() if audio_languages else {}
    hate_component_distribution = pd.Series(hate_components).value_counts().to_dict() if hate_components else {}
    
    metrics = {
        "binary_classification": binary_metrics,
        "video_language_distribution": video_language_distribution,
        "audio_language_distribution": audio_language_distribution,
        "hate_component_distribution": hate_component_distribution
    }
    
    save_metrics(metrics, "video")
    
    print(f"Video Model Evaluation Complete - F1 Score: {binary_metrics['f1_score']:.4f}")
    
    return metrics
