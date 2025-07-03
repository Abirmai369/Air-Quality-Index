"""
Module for AQI prediction using machine learning models.
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from config import DEFAULT_PREDICTION_DAYS, PREDICTION_GROWTH_RATE


class AQIPredictor:
    """Handles AQI prediction using linear regression."""
    
    def __init__(self, growth_rate=None):
        """
        Initialize the AQI predictor.
        
        Args:
            growth_rate (float, optional): Growth rate for prediction model.
                                         Defaults to config.PREDICTION_GROWTH_RATE.
        """
        self.growth_rate = growth_rate or PREDICTION_GROWTH_RATE
        self.model = LinearRegression()
    
    def predict_aqi(self, current_aqi, days=None):
        """
        Predict AQI values for the next specified number of days.
        
        Args:
            current_aqi (int): Current AQI value.
            days (int, optional): Number of days to predict. 
                                Defaults to DEFAULT_PREDICTION_DAYS.
        
        Returns:
            numpy.ndarray: Array of predicted AQI values.
        """
        if days is None:
            days = DEFAULT_PREDICTION_DAYS
        
        # Create training data based on growth pattern
        X = np.array([i + 1 for i in range(days)]).reshape(-1, 1)
        y = np.array([current_aqi * (1 + self.growth_rate * i) for i in range(days)])
        
        # Train the model
        self.model.fit(X, y)
        
        # Make predictions
        predictions = self.model.predict(X)
        
        # Ensure predictions are within valid AQI range (0-500)
        predictions = np.clip(predictions, 0, 500)
        
        return predictions
    
    def predict_multiple_cities(self, city_aqi_dict, days=None):
        """
        Predict AQI for multiple cities.
        
        Args:
            city_aqi_dict (dict): Dictionary mapping city names to current AQI values.
            days (int, optional): Number of days to predict.
        
        Returns:
            dict: Dictionary mapping city names to their prediction arrays.
        """
        predictions = {}
        for city, aqi in city_aqi_dict.items():
            if aqi is not None:
                try:
                    predictions[city] = self.predict_aqi(aqi, days)
                except Exception as e:
                    print(f"Warning: Could not predict AQI for {city}: {str(e)}")
                    predictions[city] = None
            else:
                predictions[city] = None
        return predictions
    
    def get_prediction_summary(self, current_aqi, days=None):
        """
        Get a summary of predictions including statistics.
        
        Args:
            current_aqi (int): Current AQI value.
            days (int, optional): Number of days to predict.
        
        Returns:
            dict: Dictionary containing prediction statistics.
        """
        predictions = self.predict_aqi(current_aqi, days)
        
        return {
            'predictions': predictions.tolist(),
            'min_predicted': float(np.min(predictions)),
            'max_predicted': float(np.max(predictions)),
            'avg_predicted': float(np.mean(predictions)),
            'trend': 'increasing' if predictions[-1] > predictions[0] else 'decreasing'
        }

