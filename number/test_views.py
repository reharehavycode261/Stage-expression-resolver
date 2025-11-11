import pytest
from django.urls import reverse
from django.test import RequestFactory
from unittest.mock import patch, MagicMock
from number.models import NumberData
from number.views import index

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def number_data():
    # Mock NumberData objects
    number1 = MagicMock(spec=NumberData)
    number2 = MagicMock(spec=NumberData)
    return [number1, number2]

@pytest.fixture
def mock_number_data_queryset(number_data):
    with patch('number.views.NumberData.objects.all', return_value=number_data) as mock:
        yield mock

@pytest.fixture
def mock_render():
    with patch('number.views.render') as mock:
        yield mock

def test_index_view_renders_correct_template(request_factory, mock_number_data_queryset, mock_render):
    """
    Test that the index view renders the correct template with the correct context.
    """
    request = request_factory.get(reverse('index'))
    response = index(request)

    # Assert that render was called with the correct template and context
    mock_render.assert_called_once_with(request, 'number/index.html', {'numbers': mock_number_data_queryset.return_value})
    assert response == mock_render.return_value

def test_index_view_calls_check_for_anomalies(request_factory, mock_number_data_queryset):
    """
    Test that the check_for_anomalies method is called on each NumberData instance.
    """
    request = request_factory.get(reverse('index'))
    index(request)

    # Assert that check_for_anomalies is called on each number
    for number in mock_number_data_queryset.return_value:
        number.check_for_anomalies.assert_called_once()

def test_index_view_handles_no_numbers(request_factory, mock_render):
    """
    Test that the index view handles the case where there are no NumberData instances.
    """
    with patch('number.views.NumberData.objects.all', return_value=[]) as mock_empty_queryset:
        request = request_factory.get(reverse('index'))
        response = index(request)

        # Assert that render was called with an empty list
        mock_render.assert_called_once_with(request, 'number/index.html', {'numbers': []})
        assert response == mock_render.return_value