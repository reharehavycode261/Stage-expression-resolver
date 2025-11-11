import pytest
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
from number.views import perform_cross_validation

@pytest.fixture
def mock_request():
    """Fixture for creating a mock request object."""
    return MagicMock()

@patch('number.views.cross_validate')
@patch('number.views.evaluate_model_performance')
def test_perform_cross_validation_success(mock_evaluate, mock_cross_validate, mock_request):
    """
    Test the perform_cross_validation function for successful execution.
    """
    # Mock the cross_validate function to return a dummy score
    mock_cross_validate.return_value = {'test_score': [0.8, 0.7, 0.9, 0.85, 0.75]}
    
    # Mock the evaluate_model_performance function to return a dummy performance
    mock_evaluate.return_value = {'mean_score': 0.8, 'std_dev': 0.05}

    # Call the function
    response = perform_cross_validation(mock_request)

    # Assert the response is a JsonResponse
    assert isinstance(response, JsonResponse), "The response should be a JsonResponse object."

    # Assert the response content
    expected_content = {'mean_score': 0.8, 'std_dev': 0.05}
    assert response.content == JsonResponse(expected_content).content, "The response content is not as expected."

@patch('number.views.cross_validate')
@patch('number.views.evaluate_model_performance')
def test_perform_cross_validation_cross_validate_failure(mock_evaluate, mock_cross_validate, mock_request):
    """
    Test the perform_cross_validation function when cross_validate raises an exception.
    """
    # Mock the cross_validate function to raise an exception
    mock_cross_validate.side_effect = Exception("Cross-validation error")

    # Call the function and expect an exception
    with pytest.raises(Exception) as excinfo:
        perform_cross_validation(mock_request)

    # Assert the exception message
    assert "Cross-validation error" in str(excinfo.value), "The exception message should indicate a cross-validation error."

@patch('number.views.cross_validate')
@patch('number.views.evaluate_model_performance')
def test_perform_cross_validation_evaluate_failure(mock_evaluate, mock_cross_validate, mock_request):
    """
    Test the perform_cross_validation function when evaluate_model_performance raises an exception.
    """
    # Mock the cross_validate function to return a dummy score
    mock_cross_validate.return_value = {'test_score': [0.8, 0.7, 0.9, 0.85, 0.75]}
    
    # Mock the evaluate_model_performance function to raise an exception
    mock_evaluate.side_effect = Exception("Evaluation error")

    # Call the function and expect an exception
    with pytest.raises(Exception) as excinfo:
        perform_cross_validation(mock_request)

    # Assert the exception message
    assert "Evaluation error" in str(excinfo.value), "The exception message should indicate an evaluation error."