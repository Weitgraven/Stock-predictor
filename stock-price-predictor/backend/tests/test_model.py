import unittest
from models.model import StockPriceModel
from models.training import ModelTrainer
import numpy as np

class TestModel(unittest.TestCase):
    def setUp(self):
        self.model_builder = StockPriceModel()
        self.trainer = ModelTrainer()
        self.input_shape = (60, 1)
        self.model = self.model_builder.build_lstm(self.input_shape)
        self.data = np.random.rand(100, 60, 1)
        self.labels = np.random.rand(100)

    def test_model_training(self):
        model, history = self.trainer.train_model(self.model, self.data, self.labels, batch_size=2, epochs=1)
        self.assertIsNotNone(history)
        self.assertGreater(len(history.history['loss']), 0)

    def test_model_prediction(self):
        prediction = self.model.predict(self.data[:1])
        self.assertEqual(prediction.shape, (1, 1))

if __name__ == '__main__':
    unittest.main()
