import pytest
from django.test import RequestFactory
from django.shortcuts import render
from number.views import plot_equation

@pytest.fixture
def request_factory():
    return RequestFactory()

def test_plot_equation_valid_input(request_factory):
    """
    Test plot_equation with a valid equation input.
    """
    request = request_factory.post('/plot', data={'equation': 'np.sin(x)'})
    response = plot_equation(request)
    
    # Check that the response is a valid HTTP response
    assert response.status_code == 200
    
    # Check that the plot is included in the response context
    assert 'plot' in response.context
    assert response.context['plot'] is not None

def test_plot_equation_invalid_input(request_factory):
    """
    Test plot_equation with an invalid equation input.
    """
    request = request_factory.post('/plot', data={'equation': 'invalid_equation'})
    
    # Expecting an exception due to invalid input
    with pytest.raises(Exception):
        plot_equation(request)

def test_plot_equation_empty_input(request_factory):
    """
    Test plot_equation with an empty equation input.
    """
    request = request_factory.post('/plot', data={'equation': ''})
    response = plot_equation(request)
    
    # Check that the response is a valid HTTP response
    assert response.status_code == 200
    
    # Check that the plot is None due to empty input
    assert 'plot' in response.context
    assert response.context['plot'] is None

def test_plot_equation_get_request(request_factory):
    """
    Test plot_equation with a GET request.
    """
    request = request_factory.get('/plot')
    response = plot_equation(request)
    
    # Check that the response is a valid HTTP response
    assert response.status_code == 200
    
    # Check that the plot is None for a GET request
    assert 'plot' in response.context
    assert response.context['plot'] is None