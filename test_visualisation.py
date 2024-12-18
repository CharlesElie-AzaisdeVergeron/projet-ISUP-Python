"""Tests for visualization functions using pytest."""

import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from unittest.mock import patch, MagicMock
from visualisation import heatmap

@pytest.fixture
def sample_correlation_data():
    """Fixture providing sample correlation matrix data."""
    correlation_matrix = pd.DataFrame({
        'A': [1.0, 0.5, 0.3],
        'B': [0.5, 1.0, 0.7],
        'C': [0.3, 0.7, 1.0]
    }, index=['A', 'B', 'C'])
    return correlation_matrix

@pytest.fixture
def sample_confidence_data():
    """Fixture providing sample confidence interval data."""
    coefficients = np.array([1.2, 2.3, 3.4])
    intervals = np.array([[1.0, 1.4], [2.1, 2.5], [3.2, 3.6]])
    feature_names = ['X1', 'X2', 'X3']
    return coefficients, intervals, feature_names

@pytest.mark.visualization
class TestHeatmap:
    """Test suite for heatmap visualization function."""
    
    def test_heatmap_creation(self, sample_correlation_data):
        """Test if heatmap is created successfully with valid data."""
        with patch('seaborn.heatmap') as mock_heatmap:
            mock_heatmap.return_value = MagicMock()
            fig = heatmap(sample_correlation_data)
            assert isinstance(fig, plt.Figure)
            mock_heatmap.assert_called_once()
            
    def test_heatmap_parameters(self, sample_correlation_data):
        """Test if heatmap is created with correct parameters."""
        with patch('seaborn.heatmap') as mock_heatmap:
            heatmap(sample_correlation_data)
            kwargs = mock_heatmap.call_args.kwargs
            assert kwargs.get('annot') == True
            assert kwargs.get('cmap') == 'coolwarm'
            assert kwargs.get('vmin') == -1
            assert kwargs.get('vmax') == 1
            
    def test_heatmap_empty_data(self):
        """Test heatmap behavior with empty data."""
        empty_df = pd.DataFrame()
        with pytest.raises(ValueError):
            heatmap(empty_df)
            
    def test_heatmap_nan_values(self):
        """Test heatmap handling of NaN values."""
        data_with_nan = pd.DataFrame({
            'A': [1.0, np.nan, 0.3],
            'B': [0.5, 1.0, 0.7],
            'C': [0.3, 0.7, 1.0]
        })
        with patch('seaborn.heatmap') as mock_heatmap:
            fig = heatmap(data_with_nan)
            assert isinstance(fig, plt.Figure)
            
