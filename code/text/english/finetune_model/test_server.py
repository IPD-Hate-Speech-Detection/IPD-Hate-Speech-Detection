import unittest
import json
from server import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_predict(self):
        payload = {"text": "jews are such self-serving people"}
        response = self.app.post('/predict',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertIn('hate', data['prediction'])
        self.assertGreater(data['probability'][0], 0.5)

if __name__ == '__main__':
    unittest.main()