import os

API_KEYS = [
    {
        'name': 'Alpha Vantage',
        'apikey': 'YOUR_ALPHA_VANTAGE_API_KEY',
        'url': 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apikey}&datatype=json'
    },
    # Add more APIs here if needed
]

CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')
