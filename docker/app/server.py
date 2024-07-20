from flask import Flask, jsonify, request
from transformers import pipeline

app = Flask("Hate_Speech")

@app.route("/predict", methods=['POST'])
def do_prediction():
    json = request.get_json()
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    sequence_to_classify = json["text"]
    candidate_labels = ['hate', 'not hate']
    prediction = classifier(sequence_to_classify, candidate_labels)
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)