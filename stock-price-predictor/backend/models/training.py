from sklearn.model_selection import train_test_split
from loguru import logger

class ModelTrainer:
    def train_model(self, model, data, labels, batch_size, epochs):
        try:
            X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
            history = model.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size=batch_size, epochs=epochs)
            logger.info("Model trained successfully")
            return model, history
        except Exception as e:
            logger.error(f"Error during model training: {e}")
            raise e
