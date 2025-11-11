import pytest
from unittest.mock import patch, MagicMock
from django.http import Http404
from django.test import RequestFactory
from number.views import detect_anomalies, character_detail
from number.models import Character, Anomaly

@pytest.fixture
def mock_character():
    character = MagicMock(spec=Character)
    character.detected_anomalies.all.return_value = []
    return character

@pytest.fixture
def mock_anomaly():
    anomaly = MagicMock(spec=Anomaly)
    return anomaly

@pytest.fixture
def request_factory():
    return RequestFactory()

def test_detect_anomalies_no_anomalies():
    """Test detect_anomalies with no anomalies detected."""
    data = [1, 2, 3]
    threshold = 10
    with patch('number.views.np.mean', return_value=2):
        anomalies = detect_anomalies(data)
    assert anomalies == [], "Expected no anomalies when mean is below threshold"

def test_detect_anomalies_with_anomalies():
    """Test detect_anomalies with anomalies detected."""
    data = [10, 20, 30]
    threshold = 15
    with patch('number.views.np.mean', return_value=20):
        anomalies = detect_anomalies(data)
    assert anomalies == ["Mean value too high"], "Expected anomaly when mean is above threshold"

def test_character_detail_view_success(request_factory, mock_character, mock_anomaly):
    """Test character_detail view with a valid character."""
    mock_character.pk = 1
    with patch('number.views.get_object_or_404', return_value=mock_character):
        with patch('number.views.detect_anomalies', return_value=["Mean value too high"]):
            with patch('number.views.Anomaly.objects.get_or_create', return_value=(mock_anomaly, True)):
                request = request_factory.get('/character/1/')
                response = character_detail(request, 1)
                assert response.status_code == 200, "Expected status code 200 for valid character"
                assert 'character' in response.context_data, "Expected character in context data"
                assert 'anomalies' in response.context_data, "Expected anomalies in context data"

def test_character_detail_view_not_found(request_factory):
    """Test character_detail view with a non-existent character."""
    with patch('number.views.get_object_or_404', side_effect=Http404):
        request = request_factory.get('/character/999/')
        with pytest.raises(Http404):
            character_detail(request, 999)