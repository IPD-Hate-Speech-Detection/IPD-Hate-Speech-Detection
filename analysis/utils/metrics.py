import numpy as np # type: ignore
import json
import os
from typing import List, Dict
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, roc_curve, auc # type: ignore
from config.config import METRICS_PATH

def calculate_binary_metrics(y_true: List[str], y_pred: List[str], 
                            y_scores: List[float] = None) -> Dict:
    
    if all(isinstance(label, str) for label in y_true):
        true_label_map = {'hate': 1, 'not_hate': 0}
        # pred_label_map = {'HATE-SPEECH': 1, 'NEITHER': 0, 'OFFENSIVE-LANGUAGE': 1}
        pred_label_map = {'hate': 1, 'not-hate': 0}
        y_true_bin = [true_label_map.get(label, 0) for label in y_true]
        y_pred_bin = [pred_label_map.get(label, 0) for label in y_pred]
    else:
        y_true_bin = y_true
        y_pred_bin = y_pred

    print(f"y_true_bin: {y_true_bin}")
    print(f"y_pred_bin: {y_pred_bin}")
        
    accuracy = accuracy_score(y_true_bin, y_pred_bin)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true_bin, y_pred_bin, average='binary', pos_label=1
    )
    
    metrics = {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1)
    }
    
    if y_scores:
        try:
            fpr, tpr, _ = roc_curve(y_true_bin, y_scores)
            roc_auc = auc(fpr, tpr)
            metrics['roc_auc'] = float(roc_auc)
            metrics['roc_curve'] = {'fpr': fpr.tolist(), 'tpr': tpr.tolist()}
        except:
            metrics['roc_auc'] = None
            metrics['roc_curve'] = None
    
    return metrics

def calculate_multiclass_metrics(y_true: List[str], y_pred: List[str]) -> Dict:
    classes = sorted(list(set(y_true + y_pred)))
    
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='weighted', labels=classes
    )
    
    precision_per_class, recall_per_class, f1_per_class, support_per_class = \
        precision_recall_fscore_support(y_true, y_pred, labels=classes)
    
    cm = confusion_matrix(y_true, y_pred, labels=classes)
    
    metrics = {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'classes': classes,
        'per_class': {
            'precision': {cls: float(prec) for cls, prec in zip(classes, precision_per_class)},
            'recall': {cls: float(rec) for cls, rec in zip(classes, recall_per_class)},
            'f1_score': {cls: float(f1) for cls, f1 in zip(classes, f1_per_class)},
            'support': {cls: int(sup) for cls, sup in zip(classes, support_per_class)}
        },
        'confusion_matrix': cm.tolist()
    }
    
    return metrics

def save_metrics(metrics: Dict, model_name: str) -> None:
    file_path = os.path.join(METRICS_PATH, f"{model_name}_results.json")
    with open(file_path, 'w') as f:
        json.dump(metrics, f, indent=4)
