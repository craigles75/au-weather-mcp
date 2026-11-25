import sys
import requests
import json
from typing import Optional, Dict, List, Any
from datetime import datetime
import time


class BOMWeather:
    """Bureau of Meteorology (BOM) Weather API client."""
    
    BASE_URL = "https://api.weather.bom.gov.au/v1"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def search_location(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for a location by suburb name or postcode.
        
        Args:
            query: Suburb name (e.g., 'parkdale') or postcode (e.g., '3195')
            
        Returns:
            List of location dictionaries containing geohash and other details
        """
        try:
            url = f"{self.BASE_URL}/locations"
            params = {'search': query}
            
            print(f"Searching for location: {query}", file=sys.stderr)
            print(f"URL: {url}", file=sys.stderr)
            print(f"Params: {params}", file=sys.stderr)
            
            response = self.session.get(url, params=params, timeout=10)
            print(f"Response status: {response.status_code}", file=sys.stderr)
            
            response.raise_for_status()
            
            data = response.json()
            print(f"Found {len(data.get('data', []))} locations", file=sys.stderr)
            return data.get('data', [])
            
        except requests.exceptions.Timeout:
            print(f"Timeout searching for location '{query}'", file=sys.stderr)
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error searching for location '{query}': {e}", file=sys.stderr)
            return []
    
    def get_location_geohash(self, query: str) -> Optional[str]:
        """
        Get the geohash for a location by searching for it.
        
        Args:
            query: Suburb name or postcode
            
        Returns:
            Geohash string if found, None otherwise
        """
        locations = self.search_location(query)
        if locations:
            return locations[0].get('geohash')
        return None
    
    def get_daily_forecast(self, geohash: str) -> Dict[str, Any]:
        """
        Get daily weather forecast for a location using its geohash.
        
        Args:
            geohash: Location geohash (e.g., 'r1ppv7u')
            
        Returns:
            Dictionary containing forecast data
        """
        try:
            url = f"{self.BASE_URL}/locations/{geohash}/forecasts/daily"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.Timeout:
            print(f"Timeout getting daily forecast for geohash '{geohash}'", file=sys.stderr)
            return {}
        except requests.exceptions.RequestException as e:
            print(f"Error getting daily forecast for geohash '{geohash}': {e}", file=sys.stderr)
            return {}
    
    def get_three_hourly_forecast(self, geohash: str) -> Dict[str, Any]:
        """
        Get three-hourly weather forecast for a location using its geohash.
        
        Args:
            geohash: Location geohash
            
        Returns:
            Dictionary containing three-hourly forecast data
        """
        try:
            url = f"{self.BASE_URL}/locations/{geohash}/forecasts/3-hourly"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.Timeout:
            print(f"Timeout getting three-hourly forecast for geohash '{geohash}'", file=sys.stderr)
            return {}
        except requests.exceptions.RequestException as e:
            print(f"Error getting three-hourly forecast for geohash '{geohash}': {e}", file=sys.stderr)
            return {}
    
    def get_observations(self, geohash: str) -> Dict[str, Any]:
        """
        Get current weather observations for a location using its geohash.
        
        Args:
            geohash: Location geohash
            
        Returns:
            Dictionary containing current observations
        """
        try:
            url = f"{self.BASE_URL}/locations/{geohash}/observations"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.Timeout:
            print(f"Timeout getting observations for geohash '{geohash}'", file=sys.stderr)
            return {}
        except requests.exceptions.RequestException as e:
            print(f"Error getting observations for geohash '{geohash}': {e}", file=sys.stderr)
            return {}
    
    def get_weather_for_location(self, location_query: str) -> Dict[str, Any]:
        """
        Get comprehensive weather information for a location.
        
        Args:
            location_query: Suburb name or postcode
            
        Returns:
            Dictionary containing location info, daily forecast, and observations
        """
        # First, find the location
        geohash = self.get_location_geohash(location_query)
        if not geohash:
            return {"error": f"Location '{location_query}' not found"}
        
        # Get weather data
        daily_forecast = self.get_daily_forecast(geohash)
        observations = self.get_observations(geohash)
        
        return {
            "location_query": location_query,
            "geohash": geohash,
            "daily_forecast": daily_forecast,
            "observations": observations
        }
    
    def format_daily_forecast(self, forecast_data: Dict[str, Any]) -> str:
        """
        Format daily forecast data into a readable string.
        
        Args:
            forecast_data: Raw forecast data from BOM API
            
        Returns:
            Formatted string with weather information
        """
        if not forecast_data or 'data' not in forecast_data:
            return "No forecast data available"
        
        forecast_days = forecast_data['data']
        formatted = []
        
        for day in forecast_days:
            date = day.get('date', 'Unknown date')
            temp_max = day.get('temp_max', 'N/A')
            temp_min = day.get('temp_min', 'N/A')
            short_text = day.get('short_text', 'No description')
            rain_chance = day.get('rain', {}).get('chance', 'N/A')
            rain_amount = day.get('rain', {}).get('amount', {})
            rain_max = rain_amount.get('max', 'N/A')
            
            formatted.append(f"""
Date: {date}
Temperature: {temp_min}°C - {temp_max}°C
Conditions: {short_text}
Rain chance: {rain_chance}%
Rain amount: {rain_max}mm
""")
        
        return "\n".join(formatted)


def test_weather_api():
    """Simple test function to check if the BOM API is accessible."""
    weather = BOMWeather()
    
    print("Testing BOM Weather API...", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    
    # Test with a simple location search
    print("1. Testing location search for '3195'...", file=sys.stderr)
    try:
        locations = weather.search_location("3195")
        if locations:
            print(f"✓ Found {len(locations)} locations", file=sys.stderr)
            for i, loc in enumerate(locations[:3]):  # Show first 3
                print(f"  {i+1}. {loc.get('name', 'Unknown')} (geohash: {loc.get('geohash', 'Unknown')})", file=sys.stderr)
        else:
            print("✗ No locations found", file=sys.stderr)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
    
    print("\n2. Testing with known geohash (r1ppv7u for Parkdale)...", file=sys.stderr)
    try:
        forecast = weather.get_daily_forecast("r1ppv7u")
        if forecast and 'data' in forecast:
            print(f"✓ Got forecast data with {len(forecast['data'])} days", file=sys.stderr)
            if forecast['data']:
                first_day = forecast['data'][0]
                print(f"  First day: {first_day.get('date', 'Unknown')} - {first_day.get('short_text', 'No description')}", file=sys.stderr)
        else:
            print("✗ No forecast data received", file=sys.stderr)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)


# Example usage and testing
if __name__ == "__main__":
    test_weather_api()
