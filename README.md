
# DigniFy - Detect Hate. Prevent Harm. Unite Communities.

## Project Overview
DigniFy is a pioneering technological intervention designed to combat the escalating challenge of online hate speech. Our solution leverages advanced deep learning technologies to create a comprehensive, multi-modal hate speech detection system

## How It's Developed
- English Text Model: Finetune Distil Roberta Model
- Hinglish Text Model: Finetune Distil Roberta Model
- Image Model: Use OCR For Text Extraction and feed into text models and some pre-decided hate speech symbol extraction is done
- Audio Model: Use Feature Extraction for getting all the info about the audio and STT feed into text model.
- Video Model: Combined Audio and Image Model on pre-decided frame rate(2sec/frame)

## Getting Started
- Select the model you want to run locally say english text
- cd code/english-text/deploy
- python -m venv venv
- .\venv\Scripts\activate
- pip install -r requirements.txt
- python app.py
- You can use the same step for any model : english-text, hinglish-text, image, audio, video

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


