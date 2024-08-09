import requests
import pandas as pd
from loguru import logger
from config import API_KEYS

class DataFetcher:
    def __init__(self, cache):
        self.cache = cache

    def fetch_data(self, symbol):
        cached_data = self.cache.get(symbol)
        if cached_data:
            logger.info(f"Returning cached data for {symbol}")
            return pd.DataFrame(cached_data)

        for source in API_KEYS:
            try:
                logger.info(f"Fetching data for {symbol} from {source['name']}")
                url = source['url'].format(symbol=symbol, apikey=source['apikey'])
                response = requests.get(url)
                data = response.json()
                if 'Time Series (Daily)' in data:
                    df = pd.DataFrame(data['Time Series (Daily)']).T
                    df.columns = ['open', 'high', 'low', 'close', 'volume']
                    df = df.astype(float)
                    self.cache.set(symbol, df.to_dict(), timeout=60*60)
                    return df
                else:
                    logger.error(f"Invalid API response from {source['name']} for {symbol}")
            except Exception as e:
                logger.error(f"Error fetching data from {source['name']} for {symbol}: {e}")
        return pd.DataFrame()
