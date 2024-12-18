"""Vehicle emissions data analysis module.

This module analyzes vehicle emissions data, calculating statistical coefficients
and confidence intervals, and creates visualizations of the relationships between
various vehicle characteristics.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistics_1 as stats
import visualisation as vis

vehicle = pd.read_csv("vehicles.csv")



features = vehicle[['Engine size (L)', 'Cylinders', 'Combined (L/100 km)']].values
target = vehicle['CO2 emissions (g/km)'].values

stats.calculate_coefficients(features, target)
stats.calculate_confidence_intervals(features, target)

vis.graphic()
vis.heatmap()

