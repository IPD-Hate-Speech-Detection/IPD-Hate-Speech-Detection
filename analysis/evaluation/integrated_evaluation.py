from typing import Dict
from utils.metrics import save_metrics

def perform_integrated_analysis(english_results: Dict, 
                                hinglish_results: Dict,
                                image_results: Dict,
                                # audio_results: Dict,
                                # video_results: Dict
                                ) -> Dict:
    
    print("Performing integrated analysis across modalities...")
    
    f1_scores = {
        "English Text": english_results["f1_score"],
        "Hinglish Text": hinglish_results["f1_score"],
        "Image": image_results["f1_score"],
        # "Audio": audio_results.get("binary_classification", {}).get("f1_score", 0),
        # "Video": video_results.get("binary_classification", {}).get("f1_score", 0)
    }
    
    # Analyze which modalities contribute most to detection
    component_analysis = {}
    # if "hate_component_distribution" in video_results:
    #     component_analysis = video_results["hate_component_distribution"]
    
    integrated_metrics = {
        "modality_comparison": {
            "f1_scores": f1_scores
        },
        "component_contribution": component_analysis
    }
    
    save_metrics(integrated_metrics, "integrated")
    
    print("Integrated analysis complete")
    
    return integrated_metrics
