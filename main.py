import numpy as np
import pandas as pd
import statistics_1 as stats
import visualisation as  vis

vehicle=pd.read_csv("vehicles.csv")



stats.Coef( features=['Engine size (L)', 'Cylinders', 'Combined (L/100 km)'], X = vehicle[['Engine size (L)', 'Cylinders', 'Combined (L/100 km)']].values, y = vehicle['CO2 emissions (g/km)'].values)
stats.prediction( X=vehicle[['Engine size (L)', 'Cylinders', 'Combined (L/100 km)']].values , y= vehicle['CO2 emissions (g/km)'].values )

vis.heatmap()
vis.graphic()