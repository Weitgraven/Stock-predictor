from flask import Flask, request, jsonify
from data.data_fetcher import DataFetcher
from data.preprocessing import Preprocessor
from models.model import StockPriceModel
from models.training import ModelTrainer
from models.deployment import ModelDeployment
from indicators.rsi import calculate_rsi
from indicators.bollinger_bands import calculate_bollinger_bands
from indicators.macd import calculate_macd
from flask_caching import Cache
from config import CACHE_DIR

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': CACHE_DIR})
data_fetcher = DataFetcher(cache)
preprocessor = Preprocessor()
model_builder = StockPriceModel()
trainer = ModelTrainer()
deployment = ModelDeployment()

@app.route('/fetch_data/<symbol>', methods=['GET'])
def fetch_data(symbol):
    df = data_fetcher.fetch_data(symbol)
    if df.empty:
        return jsonify({"error": "Failed to fetch data"}), 500
    return jsonify(df.to_dict())

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    symbol = data.get('symbol')
    if not symbol:
        return jsonify({"error": "No symbol provided"}), 400

    df = data_fetcher.fetch_data(symbol)
    if df.empty:
        return jsonify({"error": "Failed to fetch data"}), 500

    df = preprocessor.clean_data(df)
    df = preprocessor.create_features(df)
    scaled_data, scaler = preprocessor.normalize_data(df)

    model = model_builder.build_lstm((60, 1))
    model, _ = trainer.train_model(model, scaled_data, df['close'].values, batch_size=32, epochs=10)

    prediction = deployment.predict(model, scaler, df['close'].values, 60)
    rsi = calculate_rsi(df['close'])
    sma, upper_band, lower_band = calculate_bollinger_bands(df['close'])
    macd, signal = calculate_macd(df['close'])

    return jsonify({
        "prediction": prediction,
        "rsi": rsi.tolist(),
        "bollinger_bands": {
            "sma": sma.tolist(),
            "upper_band": upper_band.tolist(),
            "lower_band": lower_band.tolist()
        },
        "macd": {
            "macd": macd.tolist(),
            "signal": signal.tolist()
        }
    })

@app.route('/compare', methods=['POST'])
def compare_stocks():
    data = request.get_json()
    symbols = data.get('symbols')

    if not symbols or len(symbols) < 2:
        return jsonify({"error": "At least two symbols must be provided"}), 400

    comparison_data = {}

    for symbol in symbols:
        df = data_fetcher.fetch_data(symbol)
        if df.empty:
            return jsonify({"error": f"Failed to fetch data for {symbol}"}), 500

        df = preprocessor.clean_data(df)
        df = preprocessor.create_features(df)
        scaled_data, scaler = preprocessor.normalize_data(df)

        model = model_builder.build_lstm((60, 1))
        model, _ = trainer.train_model(model, scaled_data, df['close'].values, batch_size=32, epochs=10)

        prediction = deployment.predict(model, scaler, df['close'].values, 60)
        rsi = calculate_rsi(df['close'])
        sma, upper_band, lower_band = calculate_bollinger_bands(df['close'])
        macd, signal = calculate_macd(df['close'])

        comparison_data[symbol] = {
            "actual": df['close'].tolist(),
            "predicted": [prediction] * len(df),
            "dates": df.index.tolist(),
            "rsi": rsi.tolist(),
            "bollinger_bands": {
                "sma": sma.tolist(),
                "upper_band": upper_band.tolist(),
                "lower_band": lower_band.tolist()
            },
            "macd": {
                "macd": macd.tolist(),
                "signal": signal.tolist()
            }
        }

    return jsonify(comparison_data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
