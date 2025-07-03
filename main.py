"""
Main entry point for the Air Quality Index monitoring application.
"""

import sys
import argparse
from aqi_app import AQIApp


def main():
    """Main function to run the AQI application."""
    parser = argparse.ArgumentParser(description='Air Quality Index Monitor')
    parser.add_argument('--city', '-c', type=str, help='City name to check AQI for')
    parser.add_argument('--save-plots', '-s', action='store_true', 
                       help='Save visualization plots to files')
    parser.add_argument('--interactive', '-i', action='store_true', 
                       help='Run in interactive mode')
    parser.add_argument('--cities', nargs='+', 
                       help='Multiple cities to generate report for')
    parser.add_argument('--api-key', type=str, 
                       help='Custom API key for WAQI service')
    
    args = parser.parse_args()
    
    # Initialize the application
    app = AQIApp(api_key=args.api_key)
    
    try:
        if args.interactive or (not args.city and not args.cities):
            # Run in interactive mode
            app.run_interactive_mode()
            
        elif args.cities:
            # Generate report for multiple cities
            print("🌍 Generating multi-city AQI report...")
            report = app.get_multiple_cities_report(args.cities)
            
            print("\n📊 AQI Report Summary:")
            print("=" * 40)
            print(f"Total cities: {report['summary']['total_cities']}")
            print(f"Successful fetches: {report['summary']['successful_fetches']}")
            print(f"Failed fetches: {report['summary']['failed_fetches']}")
            
            if report['summary']['average_aqi'] > 0:
                print(f"Average AQI: {report['summary']['average_aqi']:.1f}")
                
                highest = report['summary']['highest_aqi_city']
                lowest = report['summary']['lowest_aqi_city']
                
                if highest:
                    print(f"Highest AQI: {highest['city']} ({highest['aqi']})")
                if lowest:
                    print(f"Lowest AQI: {lowest['city']} ({lowest['aqi']})")
            
            print("\n📋 Individual City Results:")
            print("-" * 40)
            for city, info in report['cities'].items():
                if info['status'] == 'success':
                    print(f"✅ {info['city']}: {info['current_aqi']} ({info['category']})")
                else:
                    print(f"❌ {city.capitalize()}: {info['error']}")
            
        elif args.city:
            # Single city mode
            print(f"🔍 Checking AQI for {args.city.capitalize()}...")
            app.generate_all_visualizations(args.city, save_plots=args.save_plots)
            
            if args.save_plots:
                print("✅ Plots saved successfully!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ An unexpected error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

