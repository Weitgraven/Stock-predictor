from loguru import logger

class ModelDeployment:
    def predict(self, model, scaler, data, time_step):
        try:
            input_data = scaler.transform(data[-time_step:].reshape(-1, 1)).reshape(1, time_step, 1)
            prediction = model.predict(input_data)
            logger.info("Prediction made successfully")
            return scaler.inverse_transform(prediction)[0, 0]
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise e
