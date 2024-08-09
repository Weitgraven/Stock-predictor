import os
import json
from loguru import logger

class CacheManager:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def get_cache_path(self, symbol):
        return os.path.join(self.cache_dir, f"{symbol}.json")

    def load_cache(self, symbol):
        cache_path = self.get_cache_path(symbol)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    logger.info(f"Loading cached data for {symbol}")
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load cache for {symbol}: {e}")
        return None

    def save_cache(self, symbol, data):
        cache_path = self.get_cache_path(symbol)
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f)
                logger.info(f"Cached data for {symbol} saved successfully")
        except Exception as e:
            logger.error(f"Failed to save cache for {symbol}: {e}")
