"""Vehicle emissions data analysis module.

This module analyzes vehicle emissions data, calculating statistical coefficients
and confidence intervals, and creates visualizations of the relationships between
various vehicle characteristics.
"""

import pandas as pd
import seaborn as sns

import statistics_1 as stats
import visualisation as vis

vehicle = pd.read_csv("vehicles.csv")



features = vehicle[['Engine size (L)', 'Cylinders', 'Combined (L/100 km)']].values
target = vehicle['CO2 emissions (g/km)'].values

stats.calculate_coefficients(features, target)
stats.calculate_confidence_intervals(features, target)

# Set the theme for the plots
sns.set_theme(rc={'figure.figsize': (10, 4)})

# Plot the pairplot for the first 15 columns
sns.pairplot(vehicle.iloc[:, 0:15])

vis.heatmap()
