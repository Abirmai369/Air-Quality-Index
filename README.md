# Air Quality Index (AQI) Monitor

A comprehensive Python application for monitoring and predicting Air Quality Index (AQI) values across different cities worldwide.

## Features

- 🌍 **Real-time AQI Data**: Fetch current AQI data from the World Air Quality Index API
- 📈 **Prediction Models**: Predict AQI trends for the next 7 days using machine learning
- 📊 **Rich Visualizations**: Multiple chart types including meters, heatmaps, histograms, and trend lines
- 🏙️ **Multi-city Comparison**: Compare AQI across multiple cities simultaneously
- 💾 **Export Capabilities**: Save visualizations as high-quality PNG files
- 🖥️ **Interactive Mode**: User-friendly command-line interface
- 🔧 **Modular Design**: Clean, maintainable code structure

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Abirmai369/Air-Quality-Index.git
cd Air-Quality-Index
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Get your API key from [World Air Quality Index](https://aqicn.org/api/) and update it in `config.py`

## Usage

### Interactive Mode
```bash
python main.py --interactive
```

### Single City Check
```bash
python main.py --city "New York"
```

### Multiple Cities Report
```bash
python main.py --cities "Delhi" "Beijing" "London" "Tokyo"
```

### Save Visualizations
```bash
python main.py --city "Mumbai" --save-plots
```

### Custom API Key
```bash
python main.py --city "Paris" --api-key "your_api_key_here"
```

## Module Structure

### 📁 Core Modules

- **`config.py`**: Configuration settings and constants
- **`data_fetcher.py`**: API communication and data retrieval
- **`aqi_utils.py`**: Utility functions for AQI categorization
- **`predictor.py`**: Machine learning models for AQI prediction
- **`visualizer.py`**: All visualization and plotting functions
- **`aqi_app.py`**: Main application orchestrator
- **`main.py`**: Entry point and command-line interface

### 🎨 Visualization Types

1. **AQI Meter**: Gauge-style visualization showing current AQI level
2. **Trend Line**: Line chart showing predicted AQI over time
3. **Histogram**: Distribution of AQI values across categories
4. **Heatmap**: Multi-city, multi-day AQI comparison
5. **Comparison Chart**: Bar chart comparing current AQI across cities

### 🏷️ AQI Categories

| Range | Category | Color |
|-------|----------|-------|
| 0-50 | Good | Green |
| 51-100 | Moderate | Yellow |
| 101-150 | Unhealthy for Sensitive Groups | Orange |
| 151-200 | Unhealthy | Red |
| 201-300 | Very Unhealthy | Purple |
| 301-500 | Hazardous | Maroon |

## API Configuration

The application uses the World Air Quality Index API. To get your free API key:

1. Visit [https://aqicn.org/api/](https://aqicn.org/api/)
2. Register for a free account
3. Copy your API token
4. Update the `API_KEY` in `config.py` or use the `--api-key` command line option

## Examples

### Basic Usage
```python
from aqi_app import AQIApp

# Initialize the app
app = AQIApp()

# Get AQI info for a city
city_info = app.get_city_aqi_info("Mumbai")
print(f"Current AQI: {city_info['current_aqi']}")

# Generate all visualizations
app.generate_all_visualizations("Mumbai", save_plots=True)
```

### Custom Prediction
```python
from predictor import AQIPredictor

predictor = AQIPredictor()
predictions = predictor.predict_aqi(current_aqi=85, days=10)
print(f"10-day predictions: {predictions}")
```

### Custom Visualization
```python
from visualizer import AQIVisualizer

viz = AQIVisualizer()
viz.plot_aqi_meter(aqi=120, city="Delhi", save_path="delhi_meter.png")
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- World Air Quality Index Project for providing the API
- Matplotlib and Seaborn communities for visualization tools
- Scikit-learn for machine learning capabilities

## Support

If you encounter any issues or have questions, please:
1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Include error messages and system information

---

**Note**: This application is for educational and informational purposes. AQI predictions are estimates based on simple models and should not be used for critical decision-making without consulting official sources.

