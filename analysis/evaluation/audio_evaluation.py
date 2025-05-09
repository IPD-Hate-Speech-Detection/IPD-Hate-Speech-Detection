from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import Dict
import librosa  # type: ignore
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
    
    with ThreadPoolExecutor(max_workers=1) as executor:
        for audio_path in tqdm(audio_paths, desc="Processing audio files"):
            try:
                duration = librosa.get_duration(path=audio_path)
                if duration > 30:
                    print(f"Skipping {audio_path}: duration {duration:.2f}s exceeds 30s")
                    predictions.append("not_hate")
                    scores.append(0.0)
                    continue
            except Exception as e:
                print(f"Could not load {audio_path} for duration check: {e}")
                predictions.append("not_hate")
                scores.append(0.0)
                continue

            future = executor.submit(model.predict, audio_path)

            try:
                result = future.result(timeout=600)  # wait max 3 minutes

                predictions.append(result["prediction"])
                scores.append(result["confidence"])
                if result.get("language") is not None:
                    languages.append(result["language"])

            except TimeoutError:
                print(f"Timeout processing {audio_path} (>180s), skipping")
                predictions.append("not_hate")
                scores.append(0.0)

            except Exception as e:
                print(f"Error processing {audio_path}: {e}")
                predictions.append("not_hate")
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
