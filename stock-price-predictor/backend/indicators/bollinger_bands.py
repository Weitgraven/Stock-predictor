import pandas as pd

def calculate_bollinger_bands(prices, period=20, num_std_dev=2):
    sma = prices.rolling(window=period).mean()
    std_dev = prices.rolling(window=period).std()
    upper_band = sma + (std_dev * num_std_dev)
    lower_band = sma - (std_dev * num_std_dev)
    return sma, upper_band, lower_band
