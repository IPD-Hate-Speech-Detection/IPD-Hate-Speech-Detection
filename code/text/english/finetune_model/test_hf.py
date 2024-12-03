from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import torch

model_name = "Tirath5504/IPD-finetuned-english-text"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

labels = model.config.id2label
print("Model Labels:", labels)
