# -*- coding: utf-8 -*-
"""Realestate_Prediction_OO.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17elatLe1qn9ePJg7hDcxU0pKVvveYRlD
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import LearningRateScheduler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


class DataPreprocessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_data(self):
        print("Attempting to load data...")
        if not os.path.exists(self.filepath):
            print(f"Error: The file '{self.filepath}' does not exist.")
            return
        try:
            self.df = pd.read_csv(self.filepath)
            print("Data loaded successfully.")
        except Exception as e:
            print(f"An error occurred while loading the file: {e}")

    def preprocess(self):
        # Fill missing values for specified columns with their mode
        print("filling empty cells and removing outliers...")

        for column in ['bed', 'bath', 'acre_lot', 'house_size']:
            self.df[column].fillna(self.df[column].mode()[0], inplace=True)

        # Drop rows with missing values in 'zip_code', 'city', and 'price' columns
        self.df = self.df.dropna(subset=['zip_code', 'city', 'price'])

        # Remove top and bottom 25 percentile outliers
        cols = ['bed', 'bath', 'acre_lot', 'house_size', 'price']
        Q1 = self.df[cols].quantile(0.25)
        Q3 = self.df[cols].quantile(0.75)
        IQR = Q3 - Q1
        self.df = self.df[~((self.df[cols] < (Q1 - 1.5 * IQR)) | (self.df[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

    def get_cleaned_data(self):
        return self.df

from sklearn.preprocessing import MinMaxScaler
class FeatureScaler:


    def __init__(self):
        # Initialize MinMaxScaler objects for scaling features and the target variable independently
        self.feature_scaler = MinMaxScaler()
        self.target_scaler = MinMaxScaler()
        print("FeatureScaler initialized with MinMaxScaler for both features and target.")

    def fit_transform(self, X, y):
        # Scale the features and the target variable
        print("Fitting and transforming features and target variable.")
        X_scaled = self.feature_scaler.fit_transform(X)
        y_scaled = self.target_scaler.fit_transform(y.values.reshape(-1,1))
        print("Features and target variable scaled successfully.")
        return X_scaled, y_scaled

    def inverse_transform(self, y):
        # Inverse transform the scaled target variable back to its original scale
        print("Inverse transforming the target variable.")
        return self.target_scaler.inverse_transform(y)

    def transform(self, X):
        # Transform the features using the existing scaler fit
        print("Transforming features using the existing scaler fit.")
        return self.feature_scaler.transform(X)


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import LearningRateScheduler
import tensorflow as tf

class RealEstatePricePredictor:
    def __init__(self):
        # Initialize the model upon creation of an instance of RealEstatePricePredictor
        print("Initializing the real estate price predictor model...")
        self.model = self._build_model()

    def _build_model(self):
        # Private method to build a Sequential neural network model
        print("Building the model...")
        model = Sequential([
            Dense(100, input_dim=5, activation='relu'),
            Dense(100, activation='relu'),
            Dense(100, activation='relu'),
            Dense(200, activation='relu'),
            Dense(200, activation='relu'),
            Dense(1, activation='linear')
        ])

        # Use Adam optimizer with gradient clipping
        optimizer = tf.keras.optimizers.Adam(clipvalue=0.5)

        # Compile the model
        model.compile(optimizer=optimizer, loss='mean_squared_error')
        return model

    def scheduler(self, epoch, lr):
        # Learning rate scheduler function to adjust the learning rate over epochs
        if epoch < 50:
            return lr  # No change in learning rate for the first 50 epochs
        else:
            adjusted_lr = lr * tf.math.exp(-0.1)  # Exponentially decay the learning rate
            print(f"Adjusting learning rate to {adjusted_lr:.6f}.")
            return adjusted_lr

    def train(self, X_train, y_train):
        # Train the model on the training data
        print("Starting training...")
        # Apply learning rate scheduler
        lr_schedule = LearningRateScheduler(self.scheduler)
        history = self.model.fit(X_train, y_train, epochs=100, batch_size=50, validation_split=0.2, callbacks=[lr_schedule])
        print("Training completed.")
        return history

    def predict(self, X):
        # Predict the target values for a given input
        print("Making predictions...")
        return self.model.predict(X)


import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

class ModelEvaluator:
    @staticmethod
    def evaluate(y_true, y_pred):
        """
        Evaluates the model performance and prints the evaluation metrics.
        """
        RMSE = np.sqrt(mean_squared_error(y_true, y_pred))
        MSE = mean_squared_error(y_true, y_pred)
        MAE = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)

        print(f"Model Evaluation Metrics:")
        print(f"RMSE (Root Mean Square Error): {RMSE:.2f}")
        print(f"MSE (Mean Squared Error): {MSE:.2f}")
        print(f"MAE (Mean Absolute Error): {MAE:.2f}")
        print(f"R^2 (Coefficient of Determination): {r2:.2f}")

        return RMSE, MSE, MAE, r2

    @staticmethod
    def plot_evaluation(y_true, y_pred):
        """
        Plots the actual vs. predicted values and the distribution of errors.
        """
        # Actual vs. Predicted
        plt.figure(figsize=(14, 6))

        plt.subplot(1, 2, 1)
        plt.scatter(y_true, y_pred, alpha=0.3)
        plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'k--', lw=2)  # Diagonal line
        plt.title('Actual vs. Predicted')
        plt.xlabel('Actual')
        plt.ylabel('Predicted')

        # Error Distribution
        plt.subplot(1, 2, 2)
        error = y_pred - y_true
        plt.hist(error, bins=25, alpha=0.6, color='r')
        plt.title('Prediction Error Distribution')
        plt.xlabel('Prediction Error')
        plt.ylabel('Frequency')

        plt.tight_layout()
        plt.show()


# Example of how to use these classes
data_preprocessor = DataPreprocessor('realtor_ma_only.csv')
data_preprocessor.load_data()
data_preprocessor.preprocess()
df = data_preprocessor.get_cleaned_data()

from sklearn.model_selection import train_test_split

# Assuming df is your DataFrame and the classes FeatureScaler, RealEstatePricePredictor, and ModelEvaluator are defined as discussed

selected_features = ['bed', 'bath', 'acre_lot', 'zip_code', 'house_size']
X = df[selected_features]
y = df['price']

# Initialize and fit-transform features and target using the feature scaler
feature_scaler = FeatureScaler()
X_scaled, y_scaled = feature_scaler.fit_transform(X, y)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.25)

# Initialize the predictor, train it, and make predictions on the test set
predictor = RealEstatePricePredictor()
predictor.train(X_train, y_train)

y_pred_scaled = predictor.predict(X_test)
y_pred = feature_scaler.inverse_transform(y_pred_scaled)
y_test_inv = feature_scaler.inverse_transform(y_test)

# Evaluate the model's performance and plot the evaluation
rmse, mse, mae, r2 = ModelEvaluator.evaluate(y_test_inv.flatten(), y_pred.flatten())  # Flatten arrays if necessary
ModelEvaluator.plot_evaluation(y_test_inv.flatten(), y_pred.flatten())  # Plot the

class ModelEvaluator:
    @staticmethod
    def evaluate(y_true, y_pred):
        """
        Evaluates the model performance and prints the evaluation metrics.
        """
        RMSE = np.sqrt(mean_squared_error(y_true, y_pred))
        MSE = mean_squared_error(y_true, y_pred)
        MAE = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)

        print(f"Model Evaluation Metrics:")
        print(f"RMSE (Root Mean Square Error): {RMSE:.2f}")
        print(f"MSE (Mean Squared Error): {MSE:.2f}")
        print(f"MAE (Mean Absolute Error): {MAE:.2f}")
        print(f"R^2 (Coefficient of Determination): {r2:.2f}")

        return RMSE, MSE, MAE, r2

    @staticmethod
    def plot_evaluation(y_true, y_pred):
        """
        Plots the actual vs. predicted values and the distribution of errors.
        """
        # Actual vs. Predicted
        plt.figure(figsize=(14, 6))

        plt.subplot(1, 2, 1)
        plt.scatter(y_true, y_pred, alpha=0.3)
        plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'k--', lw=2)  # Diagonal line
        plt.title('Actual vs. Predicted')
        plt.xlabel('Actual')
        plt.ylabel('Predicted')

        # # Error Distribution
        # plt.subplot(1, 2, 2)
        # error = y_pred - y_true
        # plt.hist(error, bins=25, alpha=0.6, color='r')
        # plt.title('Prediction Error Distribution')
        # plt.xlabel('Prediction Error')
        # plt.ylabel('Frequency')

        plt.tight_layout()
        plt.show()

# Evaluate the model's performance and plot the evaluation
rmse, mse, mae, r2 = ModelEvaluator.evaluate(y_test_inv.flatten(), y_pred.flatten())  # Flatten arrays if necessary
ModelEvaluator.plot_evaluation(y_test_inv.flatten(), y_pred.flatten())  # Plot the

