# DigniFy Evaluation System

This system provides a comprehensive evaluation framework for the DigniFy multi-modal multilingual hate speech detection system.

## Installation

Install the required dependencies:

```
pip install -r requirements.txt
```

## Preparing Test Data

Place your test data CSV files in the `data/` directory:

- `english_test_data.csv` - For English text evaluation
- `hinglish_test_data.csv` - For Hinglish text evaluation
- `image_test_data.csv` - For image evaluation
- `audio_test_data.csv` - For audio evaluation
- `video_test_data.csv` - For video evaluation

Each CSV file should have at least two columns:
- For text data: `text` and `label`
- For media data: `path` and `label`

## Running the Evaluation

To run all evaluations:

```
python main.py --all
```

To run specific evaluations:

```
python main.py --english --hinglish --visualize
```

Available options:
- `--english`: Evaluate English text model
- `--hinglish`: Evaluate Hinglish text model
- `--image`: Evaluate image model
- `--audio`: Evaluate audio model
- `--video`: Evaluate video model
- `--integrated`: Run integrated analysis
- `--visualize`: Generate visualizations

## Results

Evaluation results are saved to the `results/` directory:
- Metrics: `results/metrics/`
- Visualizations: `results/visualizations/`
