MODEL_URLS = {
    "english_text": "dj-dawgs-ipd/IPD-English-Text-Model",
    "hinglish_text": "dj-dawgs-ipd/IPD-Hinglish-Text-Model",
    "image": "dj-dawgs-ipd/IPD-Image-Pipeline",
    "audio": "dj-dawgs-ipd/IPD-Audio-Pipeline",
    "video": "dj-dawgs-ipd/IPD-Video-Pipeline"
}

BATCH_SIZE = 16
RANDOM_SEED = 42

DATA_PATH = "data/"
RESULTS_PATH = "results/"
METRICS_PATH = RESULTS_PATH + "metrics/"
VISUALIZATION_PATH = RESULTS_PATH + "visualizations/"

import os
for path in [DATA_PATH, RESULTS_PATH, METRICS_PATH, VISUALIZATION_PATH]:
    os.makedirs(path, exist_ok=True)
