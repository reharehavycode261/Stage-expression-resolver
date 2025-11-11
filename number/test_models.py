import pytest
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from number.models import cross_validate, evaluate_model_performance

@pytest.fixture
def sample_data():
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)
    return X, y

def test_cross_validate(sample_data):
    X, y = sample_data
    model = LogisticRegression()
    
    # Test with default cv=5
    scores = cross_validate(model, X, y)
    assert len(scores) == 5, "Should return 5 scores for 5-fold cross-validation"
    assert all(0 <= score <= 1 for score in scores), "Scores should be between 0 and 1"
    
    # Test with custom cv=3
    scores = cross_validate(model, X, y, cv=3)
    assert len(scores) == 3, "Should return 3 scores for 3-fold cross-validation"

def test_cross_validate_invalid_cv(sample_data):
    X, y = sample_data
    model = LogisticRegression()
    
    with pytest.raises(ValueError, match="k-fold cross-validation requires at least one train/test split"):
        cross_validate(model, X, y, cv=0)

def test_evaluate_model_performance():
    scores = [0.8, 0.85, 0.9, 0.75, 0.95]
    
    performance = evaluate_model_performance(scores)
    assert 'mean_accuracy' in performance, "Result should contain 'mean_accuracy'"
    assert 'std_accuracy' in performance, "Result should contain 'std_accuracy'"
    assert performance['mean_accuracy'] == np.mean(scores), "Mean accuracy should be correctly calculated"
    assert performance['std_accuracy'] == np.std(scores), "Standard deviation should be correctly calculated"

def test_evaluate_model_performance_empty_scores():
    scores = []
    
    performance = evaluate_model_performance(scores)
    assert performance['mean_accuracy'] == 0, "Mean accuracy should be 0 for empty scores"
    assert performance['std_accuracy'] == 0, "Standard deviation should be 0 for empty scores"