"""
Utility functions for AQI categorization and processing.
"""

from config import AQI_CATEGORIES


def get_aqi_category(aqi):
    """
    Get the AQI category and color for a given AQI value.
    
    Args:
        aqi (int): AQI value.
        
    Returns:
        tuple: (category_label, color_code) for the AQI value.
    """
    for low, high, label, color in AQI_CATEGORIES:
        if low <= aqi <= high:
            return label, color
    return "Unknown", "gray"


def get_aqi_color(aqi):
    """
    Get just the color code for a given AQI value.
    
    Args:
        aqi (int): AQI value.
        
    Returns:
        str: Color code for the AQI value.
    """
    _, color = get_aqi_category(aqi)
    return color


def get_aqi_label(aqi):
    """
    Get just the category label for a given AQI value.
    
    Args:
        aqi (int): AQI value.
        
    Returns:
        str: Category label for the AQI value.
    """
    label, _ = get_aqi_category(aqi)
    return label


def validate_aqi(aqi):
    """
    Validate if an AQI value is within reasonable bounds.
    
    Args:
        aqi (int/float): AQI value to validate.
        
    Returns:
        bool: True if AQI is valid, False otherwise.
    """
    try:
        aqi_val = float(aqi)
        return 0 <= aqi_val <= 500
    except (ValueError, TypeError):
        return False


def format_aqi_display(aqi, city_name):
    """
    Format AQI information for display.
    
    Args:
        aqi (int): AQI value.
        city_name (str): Name of the city.
        
    Returns:
        str: Formatted string with AQI information.
    """
    if not validate_aqi(aqi):
        return f"❌ Invalid AQI value for {city_name}: {aqi}"
    
    category, _ = get_aqi_category(aqi)
    return f"✅ Current AQI in {city_name.capitalize()}: {aqi} ({category})"

