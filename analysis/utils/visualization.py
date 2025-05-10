import os
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
from typing import List, Dict
from config.config import VISUALIZATION_PATH

def plot_confusion_matrix(conf_matrix: List[List], 
                         class_names: List[str], 
                         title: str,
                         model_name: str) -> None:

    plt.figure(figsize=(10, 8))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title(title)
    
    save_path = os.path.join(VISUALIZATION_PATH, 'confusion_matrices')
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(os.path.join(save_path, f"{model_name}_confusion_matrix.png"), dpi=300, bbox_inches='tight')
    plt.close()

def plot_roc_curve(fpr: List[float], 
                  tpr: List[float], 
                  auc_score: float,
                  model_name: str) -> None:
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'AUC = {auc_score:.3f}')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve - {model_name} Model')
    plt.legend(loc='lower right')
    
    save_path = os.path.join(VISUALIZATION_PATH, 'roc_curve')
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(os.path.join(save_path, f"{model_name}_roc_curve.png"), dpi=300, bbox_inches='tight')
    plt.close()

def plot_performance_comparison(metrics_dict: Dict[str, float], 
                               title: str, 
                               filename: str) -> None:

    plt.figure(figsize=(10, 6))
    models = list(metrics_dict.keys())
    values = list(metrics_dict.values())
    
    bars = plt.bar(models, values, color='steelblue')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom')
    
    plt.ylim(0, 1.0) 
    plt.ylabel('Score')
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    save_path = os.path.join(VISUALIZATION_PATH, 'performance_charts')
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(os.path.join(save_path, filename), dpi=300, bbox_inches='tight')
    plt.close()

def plot_distribution(distribution_dict: Dict[str, int],
                     title: str,
                     filename: str) -> None:
    plt.figure(figsize=(10, 6))
    labels = list(distribution_dict.keys())
    values = list(distribution_dict.values())
    
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title(title)
    
    save_path = os.path.join(VISUALIZATION_PATH, 'distributions')
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(os.path.join(save_path, filename), dpi=300, bbox_inches='tight')
    plt.close()

def generate_all_visualizations(results_data: Dict[str, Dict]) -> None:
    results_data.pop('integrated', None)
    print(results_data)
    for model, data in results_data.items():
        if 'confusion_matrix' in data:
            plot_confusion_matrix(
                data['confusion_matrix'],
                data.get('classes', ['not_hate', 'hate']),
                f'Confusion Matrix - {model} Model',
                model
            )
    
    for model, data in results_data.items():
        if 'roc_curve' in data and data['roc_curve'] and 'roc_auc' in data:
            plot_roc_curve(
                data['roc_curve']['fpr'],
                data['roc_curve']['tpr'],
                data['roc_auc'],
                model
            )
    
    if len(results_data) > 1:
        f1_scores = {model: data.get('f1_score', 0) for model, data in results_data.items()}
        plot_performance_comparison(
            f1_scores,
            'F1 Score Comparison Across Models',
            'f1_comparison.png'
        )
        
        accuracy_scores = {model: data.get('accuracy', 0) for model, data in results_data.items()}
        plot_performance_comparison(
            accuracy_scores,
            'Accuracy Comparison Across Models',
            'accuracy_comparison.png'
        )
    
    if 'video' in results_data and 'hate_component_distribution' in results_data['video']:
        plot_distribution(
            results_data['video']['hate_component_distribution'],
            'Hate Component Distribution in Videos',
            'video_hate_components.png'
        )
