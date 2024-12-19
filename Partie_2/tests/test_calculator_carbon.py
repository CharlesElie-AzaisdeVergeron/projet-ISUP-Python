import pytest
import pandas as pd
from unittest.mock import Mock, patch
from calculator_carbon import (
    remove_duplicates,
    retrieve_from_dict,
    calculate,
    gather_inputs,
)

@pytest.fixture
def sample_df():
    """Fixture providing a sample DataFrame for testing."""
    return pd.DataFrame({
        'Type': ['Electricity', 'Gas', 'Solar'],
        'CO2': [0.5, 0.3, 0.1]
    })

@pytest.fixture
def sample_dict():
    """Fixture providing a sample dictionary for testing."""
    return {
        'question1': 'What type of energy do you use?',
        'question2': 'How much do you consume?',
        'options': ['Electricity', 'Gas', 'Solar']
    }

def test_remove_duplicates():
    """Test the remove_duplicates function with various inputs."""
    # Test with list containing duplicates
    input_list = ['a', 'b', 'a', 'c', 'b', 'd']
    assert remove_duplicates(input_list) == ['a', 'b', 'c', 'd']
    
    # Test with empty list
    assert remove_duplicates([]) == []
    
    # Test with no duplicates
    input_list = ['x', 'y', 'z']
    assert remove_duplicates(input_list) == ['x', 'y', 'z']

def test_retrieve_from_dict(sample_df):
    """Test the retrieve_from_dict function."""
    # Test successful retrieval
    assert retrieve_from_dict('Electricity', sample_df) == 0.5
    
    # Test with non-existent key
    with pytest.raises(KeyError):
        retrieve_from_dict('NonExistent', sample_df)
    
    # Test with empty DataFrame
    empty_df = pd.DataFrame()
    with pytest.raises(KeyError):
        retrieve_from_dict('Electricity', empty_df)

@patch('calculator_carbon.input')
def test_calculate(mock_input, sample_df):
    """Test the calculate function with mocked inputs."""
    mock_input.side_effect = ['Electricity', '100', 'Computer;Laptop']
    
    questions = {
        'energy': 'What type of energy?',
        'quantity': 'How much energy?',
        'equipment': 'What equipment?'
    }
    
    energy_total, equipment_total = calculate(
        questions,
        sample_df,  # energies
        sample_df   # equipment
    )
    
    assert isinstance(energy_total, float)
    assert isinstance(equipment_total, float)
    assert energy_total == pytest.approx(50.0)  # 100 * 0.5

@patch('tkinter.Tk')
@patch('tkinter.StringVar')
def test_gather_inputs(mock_string_var, mock_tk):
    """Test the gather_inputs function with mocked tkinter."""
    mock_window = Mock()
    mock_string_var.return_value.get.return_value = 'Electricity'
    
    result = gather_inputs(mock_window, ['Electricity', 'Gas', 'Solar'])
    
    assert result is not None
    mock_window.title.assert_called_once()
    
def test_gather_inputs_validation():
    """Test input validation in gather_inputs function."""
    with pytest.raises(ValueError):
        gather_inputs(None, [])  # Should raise error for empty options
        
    with pytest.raises(TypeError):
        gather_inputs(None, None)  # Should raise error for None options

