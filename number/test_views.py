import pytest
from django.test import RequestFactory
from django.http import HttpResponse
from number.views import index, visualize_equation
import json

@pytest.fixture
def request_factory():
    return RequestFactory()

def test_index_view(request_factory):
    """Test the index view returns a 200 status code and renders the correct template."""
    request = request_factory.get('/')
    response = index(request)
    assert response.status_code == 200
    assert 'index.html' in [template.name for template in response.templates]

def test_visualize_equation_post_valid_equation(request_factory):
    """Test visualize_equation with a valid equation returns a 200 status code and a PNG image."""
    request_data = json.dumps({'equation': 'x**2'})
    request = request_factory.post('/visualize_equation', data=request_data, content_type='application/json')
    response = visualize_equation(request)
    assert response.status_code == 200
    assert response['Content-Type'] == 'text'
    assert response.content.startswith(b'data:image/png;base64,')

def test_visualize_equation_post_invalid_equation(request_factory):
    """Test visualize_equation with an invalid equation returns a 400 status code."""
    request_data = json.dumps({'equation': 'invalid_equation'})
    request = request_factory.post('/visualize_equation', data=request_data, content_type='application/json')
    response = visualize_equation(request)
    assert response.status_code == 400
    assert 'invalid syntax' in response.content.decode()

def test_visualize_equation_post_empty_equation(request_factory):
    """Test visualize_equation with an empty equation returns a 400 status code."""
    request_data = json.dumps({'equation': ''})
    request = request_factory.post('/visualize_equation', data=request_data, content_type='application/json')
    response = visualize_equation(request)
    assert response.status_code == 400
    assert 'unexpected EOF' in response.content.decode()

def test_visualize_equation_get_method_not_allowed(request_factory):
    """Test visualize_equation with a GET request returns a 405 status code."""
    request = request_factory.get('/visualize_equation')
    response = visualize_equation(request)
    assert response.status_code == 405