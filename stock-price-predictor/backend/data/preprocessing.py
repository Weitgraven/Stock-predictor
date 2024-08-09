import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from loguru import logger

class Preprocessor:
    def clean_data(self, df):
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)
        logger.info("Data cleaned successfully")
        return df

    def normalize_data(self, df):
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df[['close']].values)
        logger.info("Data normalized successfully")
        return scaled_data, scaler

    def create_features(self, df):
        df['ma_50'] = df['close'].rolling(window=50).mean()
        df['rsi'] = self.calculate_rsi(df['close'])
        logger.info("Features created successfully")
        return df

    def calculate_rsi(self, series, period=14):
        delta = series.diff(1)
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
