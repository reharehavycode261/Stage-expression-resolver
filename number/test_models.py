import pytest
import pandas as pd
import pickle
from unittest.mock import patch, mock_open, MagicMock
from number.models import ModelRetrainingPipeline
from sklearn.linear_model import LinearRegression

# Mock data for testing
MOCK_CSV_DATA = """feature1,feature2,target
1,2,3
4,5,6
7,8,9
10,11,12
"""
MOCK_MODEL = LinearRegression()

@pytest.fixture
def pipeline():
    return ModelRetrainingPipeline('mock_model_path.pkl', 'mock_data.csv', 'mock_retrained_model_path.pkl')

def test_load_data_success(pipeline):
    """Test loading data successfully."""
    with patch('pandas.read_csv', return_value=pd.read_csv(pd.compat.StringIO(MOCK_CSV_DATA))):
        pipeline.load_data()
        assert pipeline.data is not None
        assert not pipeline.data.empty
        assert 'target' in pipeline.data.columns

def test_load_data_failure(pipeline):
    """Test loading data with an invalid path."""
    with patch('pandas.read_csv', side_effect=Exception("File not found")):
        pipeline.load_data()
        assert pipeline.data is None

def test_preprocess_data(pipeline):
    """Test preprocessing data."""
    pipeline.data = pd.read_csv(pd.compat.StringIO(MOCK_CSV_DATA))
    pipeline.preprocess_data()
    assert pipeline.X_train is not None
    assert pipeline.X_test is not None
    assert pipeline.y_train is not None
    assert pipeline.y_test is not None
    assert len(pipeline.X_train) > 0
    assert len(pipeline.X_test) > 0

def test_load_model_success(pipeline):
    """Test loading model successfully."""
    with patch('builtins.open', mock_open(read_data=pickle.dumps(MOCK_MODEL))):
        with patch('pickle.load', return_value=MOCK_MODEL):
            pipeline.load_model()
            assert pipeline.model is not None
            assert isinstance(pipeline.model, LinearRegression)

def test_load_model_failure(pipeline):
    """Test loading model with an invalid path."""
    with patch('builtins.open', side_effect=Exception("File not found")):
        pipeline.load_model()
        assert pipeline.model is None

def test_retrain_model_with_existing_model(pipeline):
    """Test retraining model when model is already loaded."""
    pipeline.model = MOCK_MODEL
    pipeline.data = pd.read_csv(pd.compat.StringIO(MOCK_CSV_DATA))
    pipeline.preprocess_data()
    pipeline.retrain_model()
    assert pipeline.model is not None

def test_retrain_model_without_existing_model(pipeline):
    """Test retraining model when no model is loaded."""
    pipeline.data = pd.read_csv(pd.compat.StringIO(MOCK_CSV_DATA))
    pipeline.preprocess_data()
    pipeline.retrain_model()
    assert pipeline.model is not None
    assert isinstance(pipeline.model, LinearRegression)

def test_evaluate_model(pipeline):
    """Test evaluating model."""
    pipeline.model = MOCK_MODEL
    pipeline.data = pd.read_csv(pd.compat.StringIO(MOCK_CSV_DATA))
    pipeline.preprocess_data()
    pipeline.retrain_model()
    with patch('sklearn.metrics.mean_squared_error', return_value=0.0):
        mse = pipeline.evaluate_model()
        assert mse == 0.0