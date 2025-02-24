import unittest
from transformers import pipeline
import torch

classifier = pipeline(
    "text-classification",
    model="Tirath5504/IPD-finetuned-english-text",
    device=0 if torch.cuda.is_available() else -1
)

def classify_text(text):
    result = classifier(text)
    return result[0]['label']

class ModelTest(unittest.TestCase):
    def setUp(self):
        self.HATE = "OFFENSIVE-LANGUAGE"
        self.NON_HATE = "NEITHER"
        
    def test_nonhate_hello(self):
        self.assertEqual(classify_text("hello bro"), self.NON_HATE)
    def test_nonhate_friendly_talk(self):
        self.assertEqual(classify_text("how is your day?"), self.NON_HATE)
    def test_nonhate_teaching(self):
        self.assertEqual(classify_text("student today we are going to study how skin colors are different, for example black, white, etc."), self.NON_HATE)
    def test_nonhate_dontlike(self):
        self.assertEqual(classify_text("i don't like green vegetables"), self.NON_HATE)
    def test_hate_fuck(self):
        self.assertEqual(classify_text("fuck you bro"), self.HATE)
    def test_hate_nigga(self):
        self.assertEqual(classify_text("you know what today in the train one nigga was talking shit"), self.HATE)
    def test_hate_shit(self):
        self.assertEqual(classify_text("you know what today in the train one boy was talking shit"), self.HATE)

if __name__ == "__main__":
    unittest.main()
# run cmd : python -W ignore -m unittest -v .\EnglishText.py