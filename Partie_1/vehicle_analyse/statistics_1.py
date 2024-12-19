"""Module for performing ordinary least squares regression and statistical analysis
on vehicle data."""
import numpy as np
import pandas as pd
from scipy import stats

vehicle = pd.read_csv("vehicles.csv")

class OrdinaryLeastSquares:
    """Implements Ordinary Least Squares regression with optional intercept term."""

    def __init__(self, intercept=True):
        """Initialize OLS regression.
        Args:
            intercept (bool): Whether to include intercept term. Defaults to True.
        """
        self.intercept = intercept
        self.coeffs_ = None

    def fit(self, x_train, y):
        """Fit the OLS model to training data.
        Args:
            x_train (np.ndarray): Training features
            y (np.ndarray): Target values
        Returns:
            self: Returns instance of class
        """
        if self.intercept:
            x_train = np.hstack((np.ones((x_train.shape[0], 1)), x_train))
        self.coeffs_ = np.linalg.inv(x_train.T @ x_train) @ x_train.T @ y
        return self

    def predict(self, x_test):
        """Predict target values for test data.
        Args:
            x_test (np.ndarray): Test features
        
        Returns:
            np.ndarray: Predicted values
        """
        if self.intercept:
            x_test = np.hstack((np.ones((x_test.shape[0], 1)), x_test))
        return x_test @ self.coeffs_

    def get_coeffs(self):
        """Get the fitted coefficients.
        
        Returns:
            np.ndarray: Model coefficients
        """
        return self.coeffs_

    def determination_coefficient(self, x_data, y):
        """Calculate the coefficient of determination (R²).
        
        Args:
            x_data (np.ndarray): Input features
            y (np.ndarray): Actual target values
        
        Returns:
            float: R² value
        """
        y_pred = self.predict(x_data)
        ss_total = np.sum((y - np.mean(y)) ** 2)
        ss_res = np.sum((y - y_pred) ** 2)
        r_squared = 1 - (ss_res / ss_total)
        return r_squared

def calculate_coefficients(x_data, y):
    """Calculate regression coefficients and R² value.
    
    Args:
        x_data (np.ndarray): Input features
        y (np.ndarray): Target values
    
    Returns:
        tuple: Tuple containing coefficients and R² value
    """
    ols = OrdinaryLeastSquares(intercept=True)
    ols.fit(x_data, y)
    coeffs = ols.get_coeffs()
    print('Coefficients:', coeffs[1:])
    r_squared = ols.determination_coefficient(x_data, y)
    print('R²:', r_squared)
    return (coeffs, r_squared)


def calculate_confidence_intervals(x_data, y):
    """Calculate regression confidence intervals.
    
    Args:
        x_data (np.ndarray): Input features
        y (np.ndarray): Target values
    
    Returns:
        np.ndarray: Confidence intervals for coefficients
    """
    selected_features = ['Engine size (L)', 'Cylinders', 'Combined (L/100 km)']
    x_vehicle = vehicle[selected_features].values
    y_vehicle = vehicle['CO2 emissions (g/km)'].values
    result = calculate_coefficients(x_vehicle, y_vehicle)
    coeffs = result[0]
    x_with_intercept = np.hstack((x_data, np.ones((x_data.shape[0], 1))))
    y_pred = x_with_intercept @ coeffs
    residuals = y - y_pred

    sum_squared_residuals = np.sum(residuals**2)
    variance = sum_squared_residuals / (x_with_intercept.shape[0] - x_with_intercept.shape[1])
    var_cov_matrix = variance * np.linalg.inv(x_with_intercept.T @ x_with_intercept)
    std_errors = np.sqrt(np.diag(var_cov_matrix))
    df = x_with_intercept.shape[0] - x_with_intercept.shape[1]
    t_value = stats.t.ppf(0.975, df=df)  # 95% confidence interval
    conf_intervals = np.array([coeffs - t_value * std_errors,
                            coeffs + t_value * std_errors]).T

    print(f"1er paramètre : [{conf_intervals[1][0]:.1f} ,{conf_intervals[1][1]:.1f}]")
    print(f"2eme paramètre :[{conf_intervals[2][0]:.1f},{conf_intervals[2][1]:.1f}]")
    print(f"3eme paramètre : [{conf_intervals[3][0]:.1f},{conf_intervals[3][1]:.1f}]")

    return conf_intervals
