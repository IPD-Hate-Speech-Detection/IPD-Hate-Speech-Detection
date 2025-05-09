import pandas as pd # type: ignore
import os
from typing import List, Dict, Tuple
from config.config import DATA_PATH

def load_text_data(file_path: str) -> Tuple[List[str], List[str]]:
    df = pd.read_csv(os.path.join(DATA_PATH, file_path))
    return df['text'].tolist(), df['label'].tolist()

def load_media_data(file_path: str) -> Tuple[List[str], List[str]]:
    df = pd.read_csv(os.path.join(DATA_PATH, file_path))
    return df['path'].tolist(), df['label'].tolist()

def load_combined_test_data() -> Dict[str, Tuple[List, List]]:
    data = {}
    
    data['english'] = load_text_data('english_test_data.csv')
    data['hinglish'] = load_text_data('hinglish_test_data.csv')
    
    data['image'] = load_media_data('image_test_data.csv')
    data['audio'] = load_media_data('audio_test_data.csv')
    # data['video'] = load_media_data('video_test_data.csv')
    
    return data
