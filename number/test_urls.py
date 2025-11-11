import pytest
from django.urls import reverse
from django.test import Client
from django.http import HttpResponse

# Mocking the plot_equation_view function for testing purposes
def mock_plot_equation_view(request):
    # Simulate a successful response
    return HttpResponse("Plot generated successfully", status=200)

@pytest.fixture
def client():
    """Fixture to provide a Django test client."""
    return Client()

@pytest.fixture
def mock_view(monkeypatch):
    """Fixture to mock the plot_equation_view."""
    monkeypatch.setattr('number.views.plot_equation_view', mock_plot_equation_view)

def test_plot_equation_view_success(client, mock_view):
    """
    Test that the plot_equation_view returns a successful response.
    """
    url = reverse('plot_equation')
    response = client.get(url)
    assert response.status_code == 200
    assert response.content == b"Plot generated successfully"

def test_plot_equation_view_not_found(client):
    """
    Test that accessing a non-existent URL returns a 404 response.
    """
    url = reverse('plot_equation') + 'non-existent/'
    response = client.get(url)
    assert response.status_code == 404

def test_plot_equation_view_method_not_allowed(client, mock_view):
    """
    Test that using a POST method on the plot_equation_view returns a 405 response.
    """
    url = reverse('plot_equation')
    response = client.post(url)
    assert response.status_code == 405

def test_plot_equation_view_invalid_input(client, mock_view):
    """
    Test that providing invalid input to the plot_equation_view returns an appropriate error.
    This assumes the view handles input and returns a 400 for invalid input.
    """
    url = reverse('plot_equation')
    response = client.get(url, {'invalid_param': 'invalid_value'})
    # Assuming the view returns 400 for invalid input
    assert response.status_code == 400