"""
Example usage script demonstrating various features of the AQI Monitor.
"""

from aqi_app import AQIApp
from data_fetcher import AQIDataFetcher
from predictor import AQIPredictor
from visualizer import AQIVisualizer
from aqi_utils import format_aqi_display, get_aqi_category


def example_basic_usage():
    """Demonstrate basic AQI fetching and display."""
    print("=" * 60)
    print("EXAMPLE 1: Basic AQI Information")
    print("=" * 60)
    
    app = AQIApp()
    
    # Get AQI info for a single city
    city_info = app.get_city_aqi_info("Mumbai")
    
    if city_info['status'] == 'success':
        print(format_aqi_display(city_info['current_aqi'], city_info['city']))
        print(f"Category: {city_info['category']}")
        print(f"Predictions: {[round(x, 1) for x in city_info['predictions']]}")
    else:
        print(f"Error: {city_info['error']}")


def example_multiple_cities():
    """Demonstrate multi-city AQI comparison."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Multiple Cities Comparison")
    print("=" * 60)
    
    app = AQIApp()
    cities = ["Delhi", "Mumbai", "Beijing", "London", "New York"]
    
    report = app.get_multiple_cities_report(cities)
    
    print(f"Successfully fetched data for {report['summary']['successful_fetches']} cities")
    print(f"Average AQI: {report['summary']['average_aqi']:.1f}")
    
    if report['summary']['highest_aqi_city']:
        highest = report['summary']['highest_aqi_city']
        print(f"Highest AQI: {highest['city']} ({highest['aqi']})")
    
    if report['summary']['lowest_aqi_city']:
        lowest = report['summary']['lowest_aqi_city']
        print(f"Lowest AQI: {lowest['city']} ({lowest['aqi']})")


def example_custom_prediction():
    """Demonstrate custom prediction scenarios."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Custom Prediction Models")
    print("=" * 60)
    
    predictor = AQIPredictor()
    
    # Different scenarios
    scenarios = [
        ("Low AQI City", 45),
        ("Moderate AQI City", 85),
        ("High AQI City", 180)
    ]
    
    for scenario_name, current_aqi in scenarios:
        predictions = predictor.predict_aqi(current_aqi, days=5)
        summary = predictor.get_prediction_summary(current_aqi, days=5)
        
        print(f"\n{scenario_name} (Current AQI: {current_aqi}):")
        print(f"  5-day predictions: {[round(x, 1) for x in predictions]}")
        print(f"  Trend: {summary['trend']}")
        print(f"  Average predicted: {summary['avg_predicted']:.1f}")


def example_individual_modules():
    """Demonstrate using individual modules."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Individual Module Usage")
    print("=" * 60)
    
    # Data Fetcher
    print("Using Data Fetcher:")
    fetcher = AQIDataFetcher()
    try:
        aqi = fetcher.fetch_aqi("Tokyo")
        print(f"  Tokyo AQI: {aqi}")
    except Exception as e:
        print(f"  Error fetching Tokyo AQI: {e}")
    
    # AQI Utils
    print("\nUsing AQI Utils:")
    test_aqis = [25, 75, 125, 175, 250, 350]
    for aqi in test_aqis:
        category, color = get_aqi_category(aqi)
        print(f"  AQI {aqi}: {category} ({color})")
    
    # Predictor
    print("\nUsing Predictor:")
    predictor = AQIPredictor(growth_rate=0.02)  # Custom growth rate
    predictions = predictor.predict_aqi(100, days=3)
    print(f"  Predictions for AQI 100: {[round(x, 1) for x in predictions]}")


def example_visualization_only():
    """Demonstrate creating visualizations without fetching new data."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Visualization with Sample Data")
    print("=" * 60)
    
    visualizer = AQIVisualizer()
    
    # Sample data
    sample_aqi = 95
    sample_predictions = [98, 102, 105, 108, 112, 115, 118]
    sample_city = "Sample City"
    
    print(f"Creating visualizations for {sample_city} (AQI: {sample_aqi})")
    
    # Create individual visualizations
    try:
        # Note: In a real scenario, you might want to save these
        print("  - Creating AQI meter...")
        visualizer.plot_aqi_meter(sample_aqi, sample_city)
        
        print("  - Creating trend line...")
        import numpy as np
        visualizer.plot_trend_line(sample_aqi, np.array(sample_predictions), sample_city)
        
        print("  - Creating histogram...")
        visualizer.plot_histogram(sample_aqi, np.array(sample_predictions), sample_city)
        
        print("✅ All visualizations created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating visualizations: {e}")


def main():
    """Run all examples."""
    print("🌍 AQI Monitor - Example Usage Demonstrations")
    print("This script demonstrates various features of the AQI monitoring system.")
    
    try:
        example_basic_usage()
        example_multiple_cities()
        example_custom_prediction()
        example_individual_modules()
        example_visualization_only()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ An error occurred during examples: {e}")
        print("This might be due to API connectivity or missing dependencies.")


if __name__ == "__main__":
    main()

