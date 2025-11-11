import pytest
from django.urls import reverse
from django.test import Client
from django.http import HttpResponse

# Mocking the views module
class MockViews:
    @staticmethod
    def plot_equation(request):
        # Simulate a simple response for testing
        return HttpResponse("Plot generated", status=200)

# Replace the actual views with the mock
views = MockViews()

@pytest.fixture
def client():
    """Fixture to provide a Django test client."""
    return Client()

def test_plot_equation_success(client, monkeypatch):
    """
    Test the plot_equation view for a successful response.
    """
    # Use monkeypatch to replace the plot_equation view with the mock
    monkeypatch.setattr('number.views.plot_equation', views.plot_equation)

    url = reverse('plot_equation')
    response = client.get(url)

    assert response.status_code == 200, "Expected status code 200 for successful plot generation"
    assert response.content == b"Plot generated", "Expected response content to indicate plot generation"

def test_plot_equation_not_found(client):
    """
    Test accessing an undefined URL to ensure it returns a 404 status code.
    """
    url = reverse('plot_equation') + 'invalid/'
    response = client.get(url)

    assert response.status_code == 404, "Expected status code 404 for an invalid URL"

def test_plot_equation_method_not_allowed(client):
    """
    Test using an unsupported HTTP method on the plot_equation endpoint.
    """
    url = reverse('plot_equation')
    response = client.post(url)

    assert response.status_code == 405, "Expected status code 405 for method not allowed"