import pytest
from number.models import load, is_number, opposite, NumberData
from django.core.exceptions import ValidationError
import pickle
import os

# Mocking the Django model save method
@pytest.fixture(autouse=True)
def setup_django_db(db):
    pass

def test_load(tmpdir):
    # Create a temporary file for testing
    filename = tmpdir.join("test.pkl")
    data = {"key": "value"}
    
    # Write data to the file using pickle
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
    
    # Test if load function correctly loads the data
    loaded_data = load(filename)
    assert loaded_data == data, "The loaded data should match the original data"

def test_load_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        load("nonexistent_file.pkl")

def test_is_number():
    assert is_number("123") is True, "String '123' should be recognized as a number"
    assert is_number("123.456") is True, "String '123.456' should be recognized as a number"
    assert is_number("abc") is False, "String 'abc' should not be recognized as a number"
    assert is_number("") is False, "Empty string should not be recognized as a number"

def test_opposite():
    assert opposite('+') == '-', "Opposite of '+' should be '-'"
    assert opposite('-') == '+', "Opposite of '-' should be '+'"
    assert opposite('*') == '/', "Opposite of '*' should be '/'"
    assert opposite('/') == '*', "Opposite of '/' should be '*'"
    assert opposite('x') is None, "Opposite of 'x' should be None"

@pytest.mark.django_db
def test_number_data_check_for_anomalies():
    # Test with a normal value
    number_data = NumberData(value=500)
    number_data.check_for_anomalies()
    assert number_data.detected_anomaly is False, "Value 500 should not be detected as an anomaly"
    assert number_data.anomaly_reason is None, "Anomaly reason should be None for normal values"

    # Test with a high anomaly value
    number_data = NumberData(value=1500)
    number_data.check_for_anomalies()
    assert number_data.detected_anomaly is True, "Value 1500 should be detected as an anomaly"
    assert number_data.anomaly_reason == "Valeur hors de la plage normale", "Anomaly reason should be set for high values"

    # Test with a low anomaly value
    number_data = NumberData(value=-1500)
    number_data.check_for_anomalies()
    assert number_data.detected_anomaly is True, "Value -1500 should be detected as an anomaly"
    assert number_data.anomaly_reason == "Valeur hors de la plage normale", "Anomaly reason should be set for low values"