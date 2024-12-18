import numpy as np
import pandas as pd
import scipy.stats as stats

vehicle = pd.read_csv("vehicles.csv")

class OrdinaryLeastSquares:
    def __init__(self, intercept=True):
        self.intercept = intercept
        self.coeffs_ = None

    def fit(self, X, y):
        if self.intercept:
            X = np.hstack((np.ones((X.shape[0], 1)), X))  # Add intercept column
        # OLS estimator
        self.coeffs_ = np.linalg.inv(X.T @ X) @ X.T @ y
        return self

    def predict(self, Xt):
        if self.intercept:
            Xt = np.hstack((np.ones((Xt.shape[0], 1)), Xt))  # Add intercept column
        return Xt @ self.coeffs_

    def get_coeffs(self):
        return self.coeffs_

    def determination_coefficient(self, X, y):
        y_pred = self.predict(X)
        ss_total = np.sum((y - np.mean(y)) ** 2)
        ss_res = np.sum((y - y_pred) ** 2)
        r_squared = 1 - (ss_res / ss_total)
        return r_squared

# Loading the dataset
df = pd.read_csv('/home/leferre/Bureau/Fac/python/vehicles.csv')

def Coef(features,X,y):
    # Creating and training the OLS model
    ols = OrdinaryLeastSquares(intercept=True)
    ols.fit(X, y)
    coef = ols.get_coeffs()
# Print coefficients
    print('Coefficients:', ols.get_coeffs())

# Predicting based on the dataset
    y_pred = ols.predict(X)

# Calculating R^2
    r_squared = ols.determination_coefficient(X, y)
    print('R^2:', r_squared)
    K= (coef , r_squared)
    return K


def prediction(X,y):
    K=Coef( features=['Engine size (L)', 'Cylinders', 'Combined (L/100 km)'], X = vehicle[['Engine size (L)', 'Cylinders', 'Combined (L/100 km)']].values, y = vehicle['CO2 emissions (g/km)'].values)
    coef = K[0]
    saved_X = X
    ones_column = np.ones((X.shape[0], 1))
    X = np.hstack((saved_X, ones_column))
    y_pred = X @ coef
    residuals = y - y_pred

    # Calculer la variance des erreurs
    RSS = np.sum(residuals**2)
    variance = RSS / (X.shape[0] - X.shape[1])

    #    Calculer la matrice de variance-covariance des coefficients
    var_cov_matrix = variance * np.linalg.inv(X.T @ X)

#    Calculer les erreurs standard des coefficients
    std_errors = np.sqrt(np.diag(var_cov_matrix))

    # Obtenir les intervalles de confiance
    t_value = stats.t.ppf(1 - 0.025, df=X.shape[0] - X.shape[1])  # Pour un intervalle de confiance à 95%
    conf_intervals = np.array([coef - t_value * std_errors, coef + t_value * std_errors]).T
    print(conf_intervals)
    return conf_intervals


