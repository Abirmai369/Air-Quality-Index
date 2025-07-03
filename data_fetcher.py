"""
Module for fetching Air Quality Index data from external APIs.
"""

import requests
from config import API_KEY, BASE_URL


class AQIDataFetcher:
    """Handles fetching AQI data from the WAQI API."""
    
    def __init__(self, api_key=None):
        """
        Initialize the data fetcher.
        
        Args:
            api_key (str, optional): API key for WAQI service. 
                                   Defaults to config.API_KEY if not provided.
        """
        self.api_key = api_key or API_KEY
        self.base_url = BASE_URL
    
    def fetch_aqi(self, city):
        """
        Fetch current AQI for a given city.
        
        Args:
            city (str): Name of the city to fetch AQI for.
            
        Returns:
            int: Current AQI value for the city.
            
        Raises:
            Exception: If API request fails or city is not found.
        """
        url = f"{self.base_url}{city}/?token={self.api_key}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if response.status_code != 200 or data.get('status') != 'ok':
                raise Exception(f"Failed to fetch AQI for '{city}'. Make sure the city name is supported.")
            
            return data['data']['aqi']
            
        except requests.RequestException as e:
            raise Exception(f"Network error while fetching AQI for '{city}': {str(e)}")
        except KeyError as e:
            raise Exception(f"Unexpected API response format for '{city}': {str(e)}")
    
    def fetch_multiple_cities(self, cities):
        """
        Fetch AQI data for multiple cities.
        
        Args:
            cities (list): List of city names.
            
        Returns:
            dict: Dictionary mapping city names to their AQI values.
                  Cities with fetch errors will have None values.
        """
        results = {}
        for city in cities:
            try:
                results[city] = self.fetch_aqi(city)
            except Exception as e:
                print(f"Warning: Could not fetch AQI for {city}: {str(e)}")
                results[city] = None
        return results

