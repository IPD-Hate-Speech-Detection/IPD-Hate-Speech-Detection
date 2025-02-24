from flask import Flask, jsonify, request
from transformers import pipeline
import numpy as np
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from tensorflow import keras
from keras import layers
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib 
from tensorflow.keras.models import load_model
import pickle

nltk.download('stopwords')
nltk.download('omw-1.4')
nltk.download('wordnet')
nltk.download('punkt')

app = Flask("Hate_Speech")

try:
    model = load_model('shubham_english_text_model.h5')
except ValueError as e:
    print(f"Error: {e}")
with open('shubham_english_text_tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

def preprocess(text, tokenizer):
    lemmatizer = WordNetLemmatizer()
    vocab = set()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.lower() not in stop_words and word not in string.punctuation]
    tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens]
    vocab.update(tokens)
    preprocessed_text = ' '.join(tokens)
    X = tokenizer.texts_to_sequences(preprocessed_text)
    max_len = max(len(y) for y in X)
    X = pad_sequences(X, maxlen=max_len)
    return X

@app.route("/predict", methods=['POST'])
def do_prediction():
    json = request.get_json()
    text = json["text"]
    pred = model.predict(preprocess(text, tokenizer))
    probabilities = np.mean(pred, axis=0)
    final_class = np.argmax(probabilities)
    if final_class == 0:
        prediction = "The string is classified as hate speech."
    else:
        prediction = "The string is classified as normal speech."
    return jsonify({"prediction": prediction, "probability": probabilities.tolist()})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)