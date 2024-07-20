import unittest
import json
from app.server import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_predict(self):
        payload = {"text": "jews are such self-serving people, exactly my kind"}
        response = self.app.post('/predict',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('not hate', data['labels'])
        self.assertGreater(data['scores'][0], 0.5)

if __name__ == '__main__':
    unittest.main()