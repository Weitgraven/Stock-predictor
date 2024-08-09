import unittest
from data.preprocessing import Preprocessor
import pandas as pd

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.preprocessor = Preprocessor()
        self.df = pd.DataFrame({
            'open': [1, 2, 3, 4],
            'high': [2, 3, 4, 5],
            'low': [0, 1, 2, 3],
            'close': [1, 2, 3, 4],
            'volume': [100, 200, 300, 400]
        })

    def test_clean_data(self):
        clean_df = self.preprocessor.clean_data(self.df)
        self.assertFalse(clean_df.isnull().values.any())

    def test_normalize_data(self):
        scaled_data, _ = self.preprocessor.normalize_data(self.df)
        self.assertTrue(scaled_data.max() <= 1)
        self.assertTrue(scaled_data.min() >= 0)

    def test_create_features(self):
        df_with_features = self.preprocessor.create_features(self.df)
        self.assertIn('ma_50', df_with_features.columns)
        self.assertIn('rsi', df_with_features.columns)

if __name__ == '__main__':
    unittest.main()
