import os
import json
import argparse
from typing import Dict

from evaluation.text_evaluation import evaluate_english_model, evaluate_hinglish_model
from evaluation.image_evaluation import evaluate_image_model
from evaluation.audio_evaluation import evaluate_audio_model
from evaluation.video_evaluation import evaluate_video_model
from evaluation.integrated_evaluation import perform_integrated_analysis
from utils.visualization import generate_all_visualizations
from config.config import METRICS_PATH

def load_results() -> Dict:
    results = {}
    for filename in os.listdir(METRICS_PATH):
        if filename.endswith('_results.json'):
            model_name = filename.split('_results.json')[0]
            with open(os.path.join(METRICS_PATH, filename), 'r') as f:
                results[model_name] = json.load(f)
                if model_name == 'image':
                    results[model_name] = results[model_name]["binary_classification"]
    return results

def run_evaluation(args):
    results = {}
    
    # Evaluate English model
    if args.english or args.all:
        english_results = evaluate_english_model()
        results['english'] = english_results
    
    # Evaluate Hinglish model
    if args.hinglish or args.all:
        hinglish_results = evaluate_hinglish_model()
        results['hinglish'] = hinglish_results
    
    # Evaluate Image model
    if args.image or args.all:
        image_results = evaluate_image_model()
        results['image'] = image_results
    
    # Evaluate Audio model
    if args.audio or args.all:
        audio_results = evaluate_audio_model()
        results['audio'] = audio_results
    
    # Evaluate Video model
    if args.video or args.all:
        video_results = evaluate_video_model()
        results['video'] = video_results
    
    # Load results if not already in memory
    if not results:
        results = load_results()
    elif args.integrated or args.all:
        # Fill in any missing results from disk
        # for model in ['english', 'hinglish', 'image', 'audio', 'video']:
        for model in ['english', 'hinglish', 'image', 'audio']:
            if model not in results:
                try:
                    with open(os.path.join(METRICS_PATH, f"{model}_results.json"), 'r') as f:
                        results[model] = json.load(f)
                        if model == 'image':
                            results[model] = results[model]["binary_classification"]
                except:
                    print(f"Warning: Could not load results for {model} model")
    
    # Perform integrated analysis
    if args.integrated or args.all:
        # if all(model in results for model in ['english', 'hinglish', 'image', 'audio', 'video']):
        if all(model in results for model in ['english', 'hinglish', 'image']):
            integrated_results = perform_integrated_analysis(
                results['english'],
                results['hinglish'],
                results['image'],
                # results['audio'],
                # results['video']
            )
            results['integrated'] = integrated_results
        else:
            print("Warning: Cannot perform integrated analysis without all model results")
    
    # Generate visualizations
    if args.visualize or args.all:
        generate_all_visualizations(results)
    
    return results

def main():
    """Main function to run the evaluation system."""
    parser = argparse.ArgumentParser(description='DigniFy Evaluation System')
    parser.add_argument('--all', action='store_true', help='Run all evaluations')
    parser.add_argument('--english', action='store_true', help='Evaluate English text model')
    parser.add_argument('--hinglish', action='store_true', help='Evaluate Hinglish text model')
    parser.add_argument('--image', action='store_true', help='Evaluate image model')
    parser.add_argument('--audio', action='store_true', help='Evaluate audio model')
    parser.add_argument('--video', action='store_true', help='Evaluate video model')
    parser.add_argument('--integrated', action='store_true', help='Run integrated analysis')
    parser.add_argument('--visualize', action='store_true', help='Generate visualizations')
    
    args = parser.parse_args()
    
    # If no args specified, run all evaluations
    if not any([args.all, args.english, args.hinglish, args.image, args.audio, args.video, 
                args.integrated, args.visualize]):
        args.all = True
    
    print("DigniFy Evaluation System")
    print("========================")
    results = run_evaluation(args)
    print("\nEvaluation complete. Results saved to the results directory.")

if __name__ == "__main__":
    main()