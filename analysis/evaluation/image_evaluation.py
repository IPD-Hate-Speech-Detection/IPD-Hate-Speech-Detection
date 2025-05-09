from typing import Dict
from tqdm import tqdm # type: ignore
import pandas as pd # type: ignore
from models.image_model import ImageModel
from utils.metrics import calculate_binary_metrics, save_metrics
from utils.data_loader import load_media_data

def evaluate_image_model(test_data_path: str = "image_test_data.csv") -> Dict:
    print("Evaluating Image Model...")
    
    image_paths, true_labels = load_media_data(test_data_path)
    
    model = ImageModel()
    
    predictions = []
    scores = []
    symbol_labels = []
    
    for image_path in tqdm(image_paths, desc="Processing images"):
        result = model.predict(image_path)
        
        predictions.append(result["prediction"])
        scores.append(result["confidence"])
        
        if result["label"] is not None:
            symbol_labels.append(result["label"])
    
    binary_metrics = calculate_binary_metrics(true_labels, predictions, scores)
    
    metrics = {
        "binary_classification": binary_metrics,
    }
    
    # If we have symbol labels, evaluate symbol detection too
    if len(symbol_labels) > 0:
        symbol_counts = pd.Series(symbol_labels).value_counts().to_dict()
        metrics["symbol_distribution"] = symbol_counts
    
    save_metrics(metrics, "image")
    
    print(f"Image Model Evaluation Complete - F1 Score: {binary_metrics['f1_score']:.4f}")
    
    return metrics
