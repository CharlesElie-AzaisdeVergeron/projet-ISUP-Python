"""
Vehicle Data Visualization Module.

This module provides functions to create visualizations for vehicle data analysis,
including correlation heatmaps and pair plots using seaborn.
"""
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


# Load the vehicle dataset
vehicle = pd.read_csv('vehicles.csv')


def graphic():
    # Set the theme for the plots
    sns.set_theme(rc={'figure.figsize':(10,4)})
    
# Plot the pairplot for the first 15 columns
    sns.pairplot(vehicle.iloc[:, 0:15])
    
    plt.show()
    
    
def heatmap():
    """
    Create a correlation heatmap and pairplot of vehicle data.

    Returns:
        matplotlib.axes.Axes: The axes object containing the heatmap
    """

# Select only numeric columns for correlation
    numeric_df = vehicle.select_dtypes(include=['number'])

# Calculate the correlation matrix
    corr_matrix = numeric_df.corr()

# Set the theme for the plot
    sns.set_theme(rc={'figure.figsize':(10,8)})

    # Plot the heatmap
    ax = sns.heatmap(corr_matrix, annot=True, cmap='coolwarm',
                    xticklabels=corr_matrix.columns,
                    yticklabels=corr_matrix.columns)
    plt.show()
    return ax


