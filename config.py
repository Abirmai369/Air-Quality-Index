"""
Configuration settings for the Air Quality Index application.
"""

# API Configuration
API_KEY = "62923ce541a74e207a652347c2bc7a817c7bc1c7"
BASE_URL = "https://api.waqi.info/feed/"

# AQI Color Categories and Thresholds
AQI_CATEGORIES = [
    (0, 50, "Good", "#00e400"),
    (51, 100, "Moderate", "#ffff00"),
    (101, 150, "Unhealthy for Sensitive Groups", "#ff7e00"),
    (151, 200, "Unhealthy", "#ff0000"),
    (201, 300, "Very Unhealthy", "#8f3f97"),
    (301, 500, "Hazardous", "#7e0023"),
]

# Prediction Settings
DEFAULT_PREDICTION_DAYS = 7
PREDICTION_GROWTH_RATE = 0.04

# Visualization Settings
FIGURE_SIZE_METER = (6, 4)
FIGURE_SIZE_HEATMAP = (12, 6)
FIGURE_SIZE_HISTOGRAM = (8, 5)

# Default cities for comparison
DEFAULT_COMPARISON_CITIES = ["Delhi", "Beijing", "New York", "London"]

