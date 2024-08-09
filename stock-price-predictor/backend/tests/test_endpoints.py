import unittest
from app import app

class TestEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_fetch_data_endpoint(self):
        response = self.app.get('/fetch_data/AAPL')
        self.assertEqual(response.status_code, 200)
        self.assertIn('close', response.json)

    def test_predict_endpoint(self):
        response = self.app.post('/predict', json={'symbol': 'AAPL'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('prediction', response.json)

if __name__ == '__main__':
    unittest.main()
