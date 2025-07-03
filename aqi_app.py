"""
Main application module for the Air Quality Index monitoring system.
"""

from data_fetcher import AQIDataFetcher
from predictor import AQIPredictor
from visualizer import AQIVisualizer
from aqi_utils import format_aqi_display, get_aqi_category
from config import DEFAULT_COMPARISON_CITIES, DEFAULT_PREDICTION_DAYS


class AQIApp:
    """Main application class that orchestrates all AQI operations."""
    
    def __init__(self, api_key=None):
        """
        Initialize the AQI application.
        
        Args:
            api_key (str, optional): API key for WAQI service.
        """
        self.data_fetcher = AQIDataFetcher(api_key)
        self.predictor = AQIPredictor()
        self.visualizer = AQIVisualizer()
    
    def get_city_aqi_info(self, city):
        """
        Get comprehensive AQI information for a city.
        
        Args:
            city (str): Name of the city.
            
        Returns:
            dict: Dictionary containing AQI information and predictions.
        """
        try:
            # Fetch current AQI
            current_aqi = self.data_fetcher.fetch_aqi(city)
            
            # Get category information
            category, color = get_aqi_category(current_aqi)
            
            # Generate predictions
            predictions = self.predictor.predict_aqi(current_aqi)
            prediction_summary = self.predictor.get_prediction_summary(current_aqi)
            
            return {
                'city': city.capitalize(),
                'current_aqi': current_aqi,
                'category': category,
                'color': color,
                'predictions': predictions,
                'prediction_summary': prediction_summary,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'city': city.capitalize(),
                'error': str(e),
                'status': 'error'
            }
    
    def generate_all_visualizations(self, city, save_plots=False):
        """
        Generate all available visualizations for a city.
        
        Args:
            city (str): Name of the city.
            save_plots (bool): Whether to save plots to files.
        """
        city_info = self.get_city_aqi_info(city)
        
        if city_info['status'] == 'error':
            print(f"❌ Error: {city_info['error']}")
            return
        
        current_aqi = city_info['current_aqi']
        predictions = city_info['predictions']
        city_name = city_info['city']
        
        print(format_aqi_display(current_aqi, city_name))
        print(f"📈 Predicted AQI for next {DEFAULT_PREDICTION_DAYS} days:", 
              [round(val, 1) for val in predictions])
        
        # Generate visualizations
        save_prefix = f"{city_name.lower()}_" if save_plots else None
        
        # AQI Meter
        self.visualizer.plot_aqi_meter(
            current_aqi, city_name,
            save_path=f"{save_prefix}aqi_meter.png" if save_plots else None
        )
        
        # Histogram
        self.visualizer.plot_histogram(
            current_aqi, predictions, city_name,
            save_path=f"{save_prefix}aqi_histogram.png" if save_plots else None
        )
        
        # Trend line
        self.visualizer.plot_trend_line(
            current_aqi, predictions, city_name,
            save_path=f"{save_prefix}aqi_trend.png" if save_plots else None
        )
        
        # Multi-city comparison
        comparison_cities = [city_name] + DEFAULT_COMPARISON_CITIES
        cities_data = self.data_fetcher.fetch_multiple_cities(comparison_cities)
        predictions_data = self.predictor.predict_multiple_cities(cities_data)
        
        # Heatmap
        self.visualizer.plot_heatmap(
            cities_data, predictions_data,
            save_path=f"{save_prefix}aqi_heatmap.png" if save_plots else None
        )
        
        # Comparison chart
        self.visualizer.create_comparison_chart(
            cities_data,
            save_path=f"{save_prefix}aqi_comparison.png" if save_plots else None
        )
    
    def run_interactive_mode(self):
        """Run the application in interactive mode."""
        print("🌍 Welcome to the Air Quality Index Monitor!")
        print("=" * 50)
        
        while True:
            try:
                city = input("\nEnter your city (or 'quit' to exit): ").strip()
                
                if city.lower() in ['quit', 'exit', 'q']:
                    print("👋 Thank you for using AQI Monitor!")
                    break
                
                if not city:
                    print("❌ Please enter a valid city name.")
                    continue
                
                print(f"\n🔍 Fetching AQI data for {city.capitalize()}...")
                self.generate_all_visualizations(city.lower())
                
                # Ask if user wants to save plots
                save_choice = input("\n💾 Would you like to save the plots? (y/n): ").strip().lower()
                if save_choice in ['y', 'yes']:
                    print("💾 Saving plots...")
                    self.generate_all_visualizations(city.lower(), save_plots=True)
                    print("✅ Plots saved successfully!")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An unexpected error occurred: {str(e)}")
    
    def get_multiple_cities_report(self, cities):
        """
        Generate a comprehensive report for multiple cities.
        
        Args:
            cities (list): List of city names.
            
        Returns:
            dict: Comprehensive report with all cities' data.
        """
        report = {
            'cities': {},
            'summary': {
                'total_cities': len(cities),
                'successful_fetches': 0,
                'failed_fetches': 0,
                'average_aqi': 0,
                'highest_aqi_city': None,
                'lowest_aqi_city': None
            }
        }
        
        valid_aqis = []
        
        for city in cities:
            city_info = self.get_city_aqi_info(city)
            report['cities'][city] = city_info
            
            if city_info['status'] == 'success':
                report['summary']['successful_fetches'] += 1
                aqi = city_info['current_aqi']
                valid_aqis.append((city, aqi))
            else:
                report['summary']['failed_fetches'] += 1
        
        # Calculate summary statistics
        if valid_aqis:
            aqi_values = [aqi for _, aqi in valid_aqis]
            report['summary']['average_aqi'] = sum(aqi_values) / len(aqi_values)
            
            highest = max(valid_aqis, key=lambda x: x[1])
            lowest = min(valid_aqis, key=lambda x: x[1])
            
            report['summary']['highest_aqi_city'] = {
                'city': highest[0],
                'aqi': highest[1]
            }
            report['summary']['lowest_aqi_city'] = {
                'city': lowest[0],
                'aqi': lowest[1]
            }
        
        return report

