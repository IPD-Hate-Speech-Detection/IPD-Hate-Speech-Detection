DigniFy - Detect Hate. Prevent Harm. Unite Communities.
=====================================================

## Description
DigniFy is a pioneering technological intervention designed to combat the escalating challenge of online hate speech. Our solution leverages advanced deep learning technologies to create a comprehensive, multi-modal hate speech detection system. This system can identify and classify hate speech in various forms, including text, images, audio, and video.

## Features
* **Multi-modal hate speech detection**: DigniFy can detect hate speech in text, images, audio, and video.
* **Advanced deep learning technologies**: Our system utilizes state-of-the-art deep learning models, including finetuned Distil Roberta models for text and ResNet50 for images.
* **Comprehensive dataset**: DigniFy is trained on a diverse and extensive dataset, ensuring high accuracy and reliability.
* **User-friendly interface**: Our system provides an easy-to-use interface for users to input their data and receive accurate results.
* **Continuous learning and improvement**: DigniFy's system is designed to learn from user feedback and improve its accuracy over time.
* **Collaboration tools**: Our system enables collaboration among users, allowing them to work together to combat online hate speech.

## Technologies Used
* **Frontend**: Python, Flask
* **Backend**: Python, TensorFlow, Keras
* **Database**: Not applicable (uses pre-trained models and datasets)
* **APIs/Libraries**: transformers, easyocr, sightengine, tensorflow, keras

## Installation
```bash
# Create a new virtual environment
python -m venv venv

# Activate the virtual environment
. venv/bin/activate  # On Linux/Mac
venv\Scripts\activate  # On Windows

# Install required packages
pip install -r requirements.txt
```

## Usage Guide
1. Select the model you want to run locally (e.g., English text, Hinglish text, image, audio, or video).
2. Navigate to the corresponding directory (e.g., `code/english-text/deploy`).
3. Run the application using `python app.py`.
4. Follow the prompts to input your data and receive results.

## API Documentation
| Endpoint | Description | Input | Output |
| --- | --- | --- | --- |
| `/text` | Classify text as hate speech or not | Text string | JSON response with classification result |
| `/image` | Classify image as hate speech or not | Image file | JSON response with classification result |
| `/audio` | Classify audio as hate speech or not | Audio file | JSON response with classification result |
| `/video` | Classify video as hate speech or not | Video file | JSON response with classification result |

## Project Structure
* `code/`: Contains the source code for the project, organized by modality (text, image, audio, video).
* `data/`: Contains the datasets used for training and testing.
* `tests/`: Contains unit tests for the project.
* `requirements.txt`: Lists the dependencies required to run the project.

## Demo Video
https://github.com/user-attachments/assets/cc7707f3-99ae-4075-b815-4a78f1eabd14

## App Download Link
[DigniFy](https://drive.google.com/file/d/1DfEYDfwpJPDtAWncA0bgV9kCxFQ1-FXb/view)


## Collaborators
Tirath Bhathawala ([GitHub](https://github.com/Tirath5504)) ([Mail](mailto:tirath.bhathawala@gmail.com))
<br>
Shubham Jaiswar ([GitHub](https://github.com/shubhamjaiswar43)) ([Mail](mailto:shubhamjaiswar08@gmail.com))
<br>
Vikas Kewat ([GitHub](https://github.com/codesbyvikas)) ([Mail](mailto:vikaskewat025@gmail.com))
<br>
Siddhant Uniyal ([GitHub](https://github.com/siddhant-uniyal)) ([Mail](mailto:siddhantuniyal416@gmail.com))

## Contributing
To contribute to DigniFy, please follow these guidelines:
* Fork the repository and create a new branch for your feature or bug fix.
* Implement your changes and commit them with a descriptive message.
* Open a pull request and wait for review and approval.

## License
DigniFy is licensed under the MIT License. See `LICENSE` for details. 
