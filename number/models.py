import operator
import pickle
import numpy as np
import pandas as pd
from django.db import models
from sympy import symbols
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class ModelRetrainingPipeline:
    def __init__(self, model_path, data_path, retrained_model_path):
        self.model_path = model_path
        self.data_path = data_path
        self.retrained_model_path = retrained_model_path
        self.model = None
        self.data = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        
    def load_data(self):
        try:
            self.data = pd.read_csv(self.data_path)
            print("Data loaded successfully.")
        except Exception as e:
            print(f"Error loading data: {e}")
        
    def preprocess_data(self):
        # Example preprocessing
        self.X = self.data.drop("target", axis=1)
        self.y = self.data["target"]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        print("Data preprocessing completed.")
        
    def load_model(self):
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
        
    def retrain_model(self):
        try:
            if self.model is None:
                self.model = LinearRegression()
            self.model.fit(self.X_train, self.y_train)
            print("Model retrained successfully.")
        except Exception as e:
            print(f"Error retraining model: {e}")
        
    def evaluate_model(self):
        try:
            predictions = self.model.predict(self.X_test)
            mse = mean_squared_error(self.y_test, predictions)
            print(f"Model evaluation completed. MSE: {mse}")
        except Exception as e:
            print(f"Error evaluating model: {e}")
        
    def save_retrained_model(self):
        try:
            with open(self.retrained_model_path, 'wb') as f:
                pickle.dump(self.model, f)
            print("Retrained model saved successfully.")
        except Exception as e:
            print(f"Error saving retrained model: {e}")
        
    def run_pipeline(self):
        self.load_data()
        self.preprocess_data()
        self.load_model()
        self.retrain_model()
        self.evaluate_model()
        self.save_retrained_model()

# Exemple d'utilisation du pipeline de réentraînement
if __name__ == "__main__":
    pipeline = ModelRetrainingPipeline("path/to/existing/model.pkl", "path/to/data.csv", "path/to/save/retrained_model.pkl")
    pipeline.run_pipeline()