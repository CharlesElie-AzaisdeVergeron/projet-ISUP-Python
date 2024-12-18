"""
Test suite for statistics_1.py using pytest.
Tests OrdinaryLeastSquares class and related statistical functions.
"""

import pytest
import numpy as np
from statistics_1 import OrdinaryLeastSquares, calculate_coefficients, calculate_confidence_intervals

@pytest.fixture
def sample_data():
    """Fixture providing simple linear regression test data."""
    X = np.array([[1, 1], [1, 2], [1, 3], [1, 4]])
    y = np.array([2, 4, 6, 8])
    return X, y

@pytest.fixture
def complex_data():
    """Fixture providing more complex multiple regression test data."""
    X = np.array([[1, 1, 1], [1, 2, 2], [1, 3, 3], [1, 4, 4], [1, 5, 5]])
    y = np.array([2, 4, 6, 8, 10])
    return X, y

@pytest.mark.ols
class TestOrdinaryLeastSquares:
    """Test suite for OrdinaryLeastSquares class."""

    def test_initialization(self):
        """Test OLS initialization."""
        ols = OrdinaryLeastSquares()
        assert ols is not None
        assert not hasattr(ols, 'coefficients')

    def test_fit_simple(self, sample_data):
        """Test fitting with simple data."""
        X, y = sample_data
        ols = OrdinaryLeastSquares()
        ols.fit(X, y)
        assert hasattr(ols, 'coefficients')
        assert len(ols.coefficients) == 2
        assert ols.coefficients[0] == pytest.approx(0.0, abs=1e-10)
        assert ols.coefficients[1] == pytest.approx(2.0, abs=1e-10)

    def test_predict(self, sample_data):
        """Test prediction functionality."""
        X, y = sample_data
        ols = OrdinaryLeastSquares()
        ols.fit(X, y)
        
        predictions = ols.predict(X)
        assert len(predictions) == len(y)
        assert predictions[0] == pytest.approx(2.0, abs=1e-10)
        assert predictions[-1] == pytest.approx(8.0, abs=1e-10)

    def test_get_coeffs(self, sample_data):
        """Test coefficient retrieval."""
        X, y = sample_data
        ols = OrdinaryLeastSquares()
        ols.fit(X, y)
        
        coeffs = ols.get_coeffs()
        assert len(coeffs) == 2
        assert coeffs[0] == pytest.approx(0.0, abs=1e-10)
        assert coeffs[1] == pytest.approx(2.0, abs=1e-10)

    def test_determination_coefficient(self, sample_data):
        """Test R-squared calculation."""
        X, y = sample_data
        ols = OrdinaryLeastSquares()
        ols.fit(X, y)
        
        r_squared = ols.determination_coefficient()
        assert 0 <= r_squared <= 1
        assert r_squared == pytest.approx(1.0, abs=1e-10)

    def test_invalid_input(self):
        """Test handling of invalid input."""
        ols = OrdinaryLeastSquares()
        with pytest.raises(ValueError):
            ols.fit(np.array([[1]]), np.array([1, 2]))

@pytest.mark.coefficients
class TestCoefficientCalculations:
    """Test suite for coefficient calculations."""

    def test_calculate_coefficients(self, complex_data):
        """Test coefficient calculation function."""
        X, y = complex_data
        coeffs = calculate_coefficients(X, y)
        assert len(coeffs) == 3
        assert coeffs[0] == pytest.approx(0.0, abs=1e-10)
        assert coeffs[1] + coeffs[2] == pytest.approx(2.0, abs=1e-10)

    def test_calculate_confidence_intervals(self, complex_data):
        """Test confidence interval calculation."""
        X, y = complex_data
        intervals = calculate_confidence_intervals(X, y)
        assert isinstance(intervals, tuple)
        assert len(intervals) == 2
        assert all(len(interval) == 3 for interval in intervals)
        
    def test_invalid_confidence_intervals(self):
        """Test handling of invalid input for confidence intervals."""
        with pytest.raises(ValueError):
            calculate_confidence_intervals(
                np.array([[1]]), 
                np.array([1])
            )

@pytest.mark.error_handling
def test_error_cases():
    """Test various error cases."""
    ols = OrdinaryLeastSquares()
    
    # Test fitting with empty arrays
    with pytest.raises(ValueError):
        ols.fit(np.array([]), np.array([]))
        
    # Test prediction without fitting
    with pytest.raises(AttributeError):
        ols.predict(np.array([[1, 1]]))
        
    # Test mismatched dimensions
    with pytest.raises(ValueError):
        ols.fit(np.array([[1, 1]]), np.array([1, 2]))

