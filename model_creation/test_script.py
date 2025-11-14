import pytest
import os
from unittest.mock import patch, MagicMock
from model_creation.script import get_directories_in, get_images_in, cross_validate_model, evaluate_model_performance
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

def test_get_directories_in(tmp_path):
    # Setup
    (tmp_path / 'dir1').mkdir()
    (tmp_path / 'dir2').mkdir()
    (tmp_path / 'file.txt').write_text("This is a file.")

    # Execute
    directories = get_directories_in(tmp_path)

    # Assert
    assert len(directories) == 2
    assert str(tmp_path / 'dir1') in directories
    assert str(tmp_path / 'dir2') in directories

def test_get_directories_in_no_directories(tmp_path):
    # Setup
    (tmp_path / 'file.txt').write_text("This is a file.")

    # Execute
    directories = get_directories_in(tmp_path)

    # Assert
    assert len(directories) == 0

def test_get_images_in(tmp_path):
    # Setup
    img_path = tmp_path / 'image.jpg'
    img_path.write_bytes(b"fake image data")
    with patch('PIL.Image.open', return_value='image_object') as mock_open:
        # Execute
        images = get_images_in(tmp_path)

        # Assert
        assert len(images) == 1
        assert images[0] == 'image_object'
        mock_open.assert_called_once_with(img_path)

def test_get_images_in_no_images(tmp_path):
    # Setup
    (tmp_path / 'file.txt').write_text("This is a file.")

    # Execute
    images = get_images_in(tmp_path)

    # Assert
    assert len(images) == 0

def test_cross_validate_model():
    # Setup
    model = RandomForestClassifier()
    X = pd.DataFrame(np.random.rand(10, 4))
    y = pd.Series(np.random.randint(0, 2, size=10))

    # Execute
    scores = cross_validate_model(model, X, y, cv=3)

    # Assert
    assert len(scores) == 3
    assert all(isinstance(score, float) for score in scores)

def test_cross_validate_model_invalid_cv():
    # Setup
    model = RandomForestClassifier()
    X = pd.DataFrame(np.random.rand(10, 4))
    y = pd.Series(np.random.randint(0, 2, size=10))

    # Execute & Assert
    with pytest.raises(ValueError):
        cross_validate_model(model, X, y, cv=0)

def test_evaluate_model_performance():
    # Setup
    model = RandomForestClassifier()
    X_train = pd.DataFrame(np.random.rand(8, 4))
    X_test = pd.DataFrame(np.random.rand(2, 4))
    y_train = pd.Series(np.random.randint(0, 2, size=8))
    y_test = pd.Series(np.random.randint(0, 2, size=2))

    # Execute
    performance_metrics = evaluate_model_performance(model, X_train, X_test, y_train, y_test)

    # Assert
    assert 'accuracy' in performance_metrics
    assert 'precision' in performance_metrics
    assert 'recall' in performance_metrics
    assert 'f1_score' in performance_metrics
    assert all(isinstance(value, float) for value in performance_metrics.values())

def test_evaluate_model_performance_invalid_data():
    # Setup
    model = RandomForestClassifier()
    X_train = pd.DataFrame(np.random.rand(8, 4))
    X_test = pd.DataFrame(np.random.rand(2, 4))
    y_train = pd.Series(np.random.randint(0, 2, size=8))
    y_test = pd.Series(np.random.randint(0, 3, size=2))  # Invalid label

    # Execute & Assert
    with pytest.raises(ValueError):
        evaluate_model_performance(model, X_train, X_test, y_train, y_test)