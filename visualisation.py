import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


vehicle = pd.read_csv('vehicles.csv')

def heatmap():
# Set the theme for the plots
    sns.set_theme(rc={'figure.figsize':(10,4)})

# Plot the pairplot for the first 10 columns
    sns.pairplot(vehicle.iloc[:, 0:15])


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

def graphic():
    # Set the theme for the plots
    sns.set_theme(rc={'figure.figsize':(10,4)})

    # Plot the pairplot for the first 10 columns
    sns.pairplot(vehicle.iloc[:, 0:15])