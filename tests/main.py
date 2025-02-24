import unittest

class ModelTest(unittest.TestCase):
    def __init__(self, text, methodName='test_upper'):
        super().__init__(methodName)  # Properly initialize unittest
        self.text = text

    def test_upper(self):
        self.assertEqual(self.text.upper(), "HELLO")

if __name__ == "__main__":
    unittest.main()
