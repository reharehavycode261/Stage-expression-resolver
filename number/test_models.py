import pytest
from django.core.exceptions import ValidationError
from number.models import AnomalyOutlier, load, is_number, opposite
import os
import pickle

# Test for the AnomalyOutlier model
@pytest.mark.django_db
def test_anomaly_outlier_creation():
    """Test creation of AnomalyOutlier instance."""
    anomaly = AnomalyOutlier.objects.create(
        name="Test Anomaly",
        description="This is a test anomaly.",
        severity=5,
        active=True
    )
    assert anomaly.name == "Test Anomaly"
    assert anomaly.description == "This is a test anomaly."
    assert anomaly.severity == 5
    assert anomaly.active is True

@pytest.mark.django_db
def test_anomaly_outlier_str():
    """Test the string representation of AnomalyOutlier."""
    anomaly = AnomalyOutlier(name="Test Anomaly")
    assert str(anomaly) == "Test Anomaly"

# Test for the load function
def test_load_function(tmp_path):
    """Test loading a pickled object."""
    test_data = {"key": "value"}
    file_path = tmp_path / "test.pkl"
    with open(file_path, 'wb') as f:
        pickle.dump(test_data, f)

    loaded_data = load(file_path)
    assert loaded_data == test_data

def test_load_function_file_not_found():
    """Test load function with a non-existent file."""
    with pytest.raises(FileNotFoundError):
        load("non_existent_file.pkl")

# Test for the is_number function
def test_is_number_valid():
    """Test is_number with valid numbers."""
    assert is_number("123") is True
    assert is_number("123.456") is True
    assert is_number("-123.456") is True

def test_is_number_invalid():
    """Test is_number with invalid numbers."""
    assert is_number("abc") is False
    assert is_number("") is False
    assert is_number("123abc") is False

# Test for the opposite function
def test_opposite_valid():
    """Test opposite function with valid operators."""
    assert opposite('+') == '-'
    assert opposite('-') == '+'
    assert opposite('*') == '/'
    assert opposite('/') == '*'

def test_opposite_invalid():
    """Test opposite function with invalid operator."""
    assert opposite('%') is None
    assert opposite('') is None
    assert opposite(None) is None