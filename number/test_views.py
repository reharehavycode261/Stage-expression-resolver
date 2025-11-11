import pytest
from django.urls import reverse
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from number.models import Character, AnomalyOutlier

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def character_image():
    # Create a simple black square image for testing
    image = Image.new('RGB', (10, 10), color='black')
    byte_arr = BytesIO()
    image.save(byte_arr, format='PNG')
    return SimpleUploadedFile("test.png", byte_arr.getvalue(), content_type="image/png")

@pytest.mark.django_db
def test_index_post_success(client, character_image, mocker):
    # Mock the get_prediction and get_solution methods
    mocker.patch('number.models.Character.get_prediction', return_value='mocked_prediction')
    mocker.patch('number.models.Character.get_solution', return_value=('step1', 'result1', 'sep1'))
    
    response = client.post(reverse('index'), {'image': character_image})
    
    assert response.status_code == 200
    assert response.json() == {
        'steps': 'step1',
        'result': 'result1',
        'separation': 'sep1'
    }

@pytest.mark.django_db
def test_index_post_no_image(client):
    response = client.post(reverse('index'))
    
    assert response.status_code == 400  # Assuming the view should return 400 if no image is provided

@pytest.mark.django_db
def test_anomaly_list(client):
    # Create some active and inactive anomalies
    AnomalyOutlier.objects.create(active=True)
    AnomalyOutlier.objects.create(active=False)
    
    response = client.get(reverse('anomaly_list'))
    
    assert response.status_code == 200
    assert len(response.context['anomalies']) == 1  # Only one active anomaly should be returned

@pytest.mark.django_db
def test_anomaly_detail_success(client):
    anomaly = AnomalyOutlier.objects.create(active=True)
    
    response = client.get(reverse('anomaly_detail', args=[anomaly.pk]))
    
    assert response.status_code == 200
    assert response.context['anomaly'] == anomaly

@pytest.mark.django_db
def test_anomaly_detail_not_found(client):
    response = client.get(reverse('anomaly_detail', args=[999]))
    
    assert response.status_code == 404  # Should return 404 if anomaly is not found