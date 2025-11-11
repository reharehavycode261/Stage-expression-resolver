import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    url = reverse('rest_register')
    data = {
        'username': 'testuser',
        'password1': 'strong_password_123',
        'password2': 'strong_password_123'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_user_login():
    client = APIClient()
    # Assuming user has been registered previously
    # Register a new user for login test
    client.post(reverse('rest_register'), {
        'username': 'testuser_login',
        'password1': 'strong_password_123',
        'password2': 'strong_password_123'
    })
    login_response = client.post(reverse('rest_login'), {
        'username': 'testuser_login',
        'password': 'strong_password_123'
    })
    assert login_response.status_code == status.HTTP_200_OK