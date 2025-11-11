import pytest
from django.test import RequestFactory
from django.http import HttpResponse
from unittest.mock import patch
from number.views import plot_equation_view

@pytest.fixture
def request_factory():
    return RequestFactory()

def test_plot_equation_view_get_request(request_factory):
    """
    Test that a GET request returns the correct template.
    """
    request = request_factory.get('/plot-equation/')
    response = plot_equation_view(request)
    assert response.status_code == 200
    assert 'index.html' in response.content.decode()

def test_plot_equation_view_post_request_default_equation(request_factory):
    """
    Test that a POST request with no equation returns a plot of x**2.
    """
    request = request_factory.post('/plot-equation/', data={})
    response = plot_equation_view(request)
    assert response.status_code == 200
    assert response['Content-Type'] == 'image/png'
    assert isinstance(response, HttpResponse)

def test_plot_equation_view_post_request_custom_equation(request_factory):
    """
    Test that a POST request with a custom equation returns the correct plot.
    """
    request = request_factory.post('/plot-equation/', data={'equation': 'x**3'})
    response = plot_equation_view(request)
    assert response.status_code == 200
    assert response['Content-Type'] == 'image/png'
    assert isinstance(response, HttpResponse)

def test_plot_equation_view_post_request_invalid_equation(request_factory):
    """
    Test that a POST request with an invalid equation raises an exception.
    """
    request = request_factory.post('/plot-equation/', data={'equation': 'invalid_equation'})
    with pytest.raises(Exception):
        plot_equation_view(request)

@patch('number.views.plt.savefig')
def test_plot_equation_view_plot_saving(mock_savefig, request_factory):
    """
    Test that the plot is saved as a PNG file.
    """
    request = request_factory.post('/plot-equation/', data={'equation': 'x**2'})
    plot_equation_view(request)
    mock_savefig.assert_called_once()
    assert mock_savefig.call_args[1]['format'] == 'png'