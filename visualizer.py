"""
Module for creating various AQI visualizations.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Wedge
from matplotlib.colors import ListedColormap

from config import (
    AQI_CATEGORIES, 
    FIGURE_SIZE_METER, 
    FIGURE_SIZE_HEATMAP, 
    FIGURE_SIZE_HISTOGRAM
)
from aqi_utils import get_aqi_category


class AQIVisualizer:
    """Handles all AQI visualization tasks."""
    
    def __init__(self):
        """Initialize the visualizer with default settings."""
        self.aqi_categories = AQI_CATEGORIES
    
    def plot_aqi_meter(self, aqi, city, save_path=None):
        """
        Create an AQI meter visualization.
        
        Args:
            aqi (int): Current AQI value.
            city (str): City name.
            save_path (str, optional): Path to save the plot. If None, displays the plot.
        """
        fig, ax = plt.subplots(figsize=FIGURE_SIZE_METER, subplot_kw={'aspect': 'equal'})
        
        # Create colored wedges for each AQI category
        wedges = []
        for i, (low, high, label, color) in enumerate(self.aqi_categories):
            start = (low / 500) * 180
            end = (high / 500) * 180
            wedge = Wedge(center=(0, 0), r=1, theta1=start, theta2=end, facecolor=color)
            wedges.append(wedge)
            ax.add_patch(wedge)
        
        # Add needle pointing to current AQI
        angle = (aqi / 500) * 180
        ax.plot([0, np.cos(np.radians(180 - angle))], [0, np.sin(np.radians(180 - angle))],
                lw=3, color="black")
        
        # Add AQI value text
        ax.text(0, -0.1, f"AQI: {aqi}", ha='center', va='center', fontsize=14, fontweight='bold')
        
        # Set plot properties
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-0.1, 1.1)
        ax.axis('off')
        plt.title(f"Current AQI Level in {city}", pad=20, fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    
    def plot_heatmap(self, cities_data, predictions_data, days=7, save_path=None):
        """
        Create a heatmap showing AQI predictions for multiple cities.
        
        Args:
            cities_data (dict): Dictionary mapping city names to current AQI values.
            predictions_data (dict): Dictionary mapping city names to prediction arrays.
            days (int): Number of prediction days.
            save_path (str, optional): Path to save the plot.
        """
        data = []
        city_names = []
        
        for city, current_aqi in cities_data.items():
            if current_aqi is not None and predictions_data.get(city) is not None:
                predictions = predictions_data[city]
                row_data = [current_aqi] + list(predictions)
                data.append(row_data)
                city_names.append(city)
            else:
                # Handle missing data
                row_data = [None] * (days + 1)
                data.append(row_data)
                city_names.append(city)
        
        if not data:
            print("No valid data available for heatmap visualization.")
            return
        
        arr = np.array(data, dtype=np.float64)
        labels = ["Today"] + [f"Day {i+1}" for i in range(days)]
        
        plt.figure(figsize=FIGURE_SIZE_HEATMAP)
        sns.heatmap(arr, annot=True, fmt=".1f", cmap="YlOrRd", 
                   xticklabels=labels, yticklabels=city_names,
                   cbar_kws={'label': 'AQI Value'})
        plt.title("AQI Prediction Heatmap", fontsize=16, fontweight='bold', pad=20)
        plt.xlabel("Time Period", fontsize=12)
        plt.ylabel("City", fontsize=12)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    
    def plot_histogram(self, current_aqi, predicted_aqi, city, save_path=None):
        """
        Create a histogram showing AQI distribution forecast.
        
        Args:
            current_aqi (int): Current AQI value.
            predicted_aqi (numpy.ndarray): Array of predicted AQI values.
            city (str): City name.
            save_path (str, optional): Path to save the plot.
        """
        values = [current_aqi] + predicted_aqi.tolist()
        bins = [0, 50, 100, 150, 200, 300, 500]
        labels = ['Good', 'Moderate', 'Unhealthy(S)', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
        
        plt.figure(figsize=FIGURE_SIZE_HISTOGRAM)
        n, bins_used, patches = plt.hist(values, bins=bins, edgecolor='black', 
                                        color='skyblue', alpha=0.7)
        
        # Color bars according to AQI categories
        for i, patch in enumerate(patches):
            if i < len(self.aqi_categories):
                patch.set_facecolor(self.aqi_categories[i][3])
        
        plt.xticks(bins[:-1], labels, rotation=45)
        plt.xlabel('AQI Category', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.title(f'AQI Distribution Forecast for {city}', fontsize=14, fontweight='bold')
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    
    def plot_trend_line(self, current_aqi, predicted_aqi, city, save_path=None):
        """
        Create a line plot showing AQI trend over time.
        
        Args:
            current_aqi (int): Current AQI value.
            predicted_aqi (numpy.ndarray): Array of predicted AQI values.
            city (str): City name.
            save_path (str, optional): Path to save the plot.
        """
        days = len(predicted_aqi)
        x_values = list(range(days + 1))
        y_values = [current_aqi] + predicted_aqi.tolist()
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, marker='o', linewidth=2, markersize=6)
        
        # Color the line segments based on AQI categories
        for i in range(len(y_values)):
            category, color = get_aqi_category(y_values[i])
            plt.scatter(x_values[i], y_values[i], color=color, s=100, zorder=5)
        
        plt.xlabel('Days', fontsize=12)
        plt.ylabel('AQI Value', fontsize=12)
        plt.title(f'AQI Trend Forecast for {city}', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # Add horizontal lines for AQI category boundaries
        for low, high, label, color in self.aqi_categories:
            if low > 0:  # Don't draw line at 0
                plt.axhline(y=low, color=color, linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    
    def create_comparison_chart(self, cities_data, save_path=None):
        """
        Create a bar chart comparing current AQI across multiple cities.
        
        Args:
            cities_data (dict): Dictionary mapping city names to current AQI values.
            save_path (str, optional): Path to save the plot.
        """
        # Filter out None values
        valid_data = {city: aqi for city, aqi in cities_data.items() if aqi is not None}
        
        if not valid_data:
            print("No valid data available for comparison chart.")
            return
        
        cities = list(valid_data.keys())
        aqi_values = list(valid_data.values())
        colors = [get_aqi_category(aqi)[1] for aqi in aqi_values]
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(cities, aqi_values, color=colors, edgecolor='black', alpha=0.8)
        
        # Add value labels on bars
        for bar, value in zip(bars, aqi_values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                    f'{value}', ha='center', va='bottom', fontweight='bold')
        
        plt.xlabel('Cities', fontsize=12)
        plt.ylabel('AQI Value', fontsize=12)
        plt.title('Current AQI Comparison Across Cities', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

