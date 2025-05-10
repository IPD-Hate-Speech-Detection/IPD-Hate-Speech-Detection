from typing import Dict
from tqdm import tqdm # type: ignore
from models.english_model import EnglishTextModel
from models.hinglish_model import HinglishTextModel
from utils.metrics import calculate_binary_metrics, calculate_multiclass_metrics, save_metrics
from utils.data_loader import load_text_data

def evaluate_english_model(test_data_path: str = "english_test_data.csv") -> Dict:
    print("Evaluating English Text Model...")
    
    texts, true_labels = load_text_data(test_data_path)
    
    model = EnglishTextModel()
    
    predictions = []
    scores = []
    
    for text in tqdm(texts, desc="Processing English texts"):
        label, score = model.predict(text)
        # print(text, label, score)
        predictions.append(label)
        scores.append(score)
    
    metrics = calculate_binary_metrics(true_labels, predictions, scores)
    
    save_metrics(metrics, "english")
    
    print(f"English Model Evaluation Complete - F1 Score: {metrics['f1_score']:.4f}")
    
    return metrics

def evaluate_hinglish_model(test_data_path: str = "hinglish_test_data.csv") -> Dict:
    print("Evaluating Hinglish Text Model...")
    
    texts, true_labels = load_text_data(test_data_path)
    
    model = HinglishTextModel()
    
    predictions = []
    scores = []
    
    for text in tqdm(texts, desc="Processing Hinglish texts"):
        label, score = model.predict(text)
        print(text, label, score)
        predictions.append(label)
        scores.append(score)
    
    # Determine if this is binary or multiclass based on the labels
    unique_labels = set(true_labels)
    if len(unique_labels) == 2 and set(unique_labels).issubset({'hate', 'not_hate'}):
        metrics = calculate_binary_metrics(true_labels, predictions, scores)
    else:
        # For multiclass (OAG, CAG, NAG)
        metrics = calculate_multiclass_metrics(true_labels, predictions)
    
    save_metrics(metrics, "hinglish")
    
    if 'f1_score' in metrics:
        print(f"Hinglish Model Evaluation Complete - F1 Score: {metrics['f1_score']:.4f}")
    else:
        print(f"Hinglish Model Evaluation Complete - Accuracy: {metrics['accuracy']:.4f}")
    
    return metrics
