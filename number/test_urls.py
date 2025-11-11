import pytest
from django.urls import reverse, resolve
from number import views

@pytest.mark.django_db
class TestUrls:
    def test_index_url_resolves(self):
        """
        Test if the root URL resolves to the index view.
        """
        url = reverse('index')
        assert resolve(url).func == views.index

    def test_anomaly_list_url_resolves(self):
        """
        Test if the anomalies URL resolves to the anomaly_list view.
        """
        url = reverse('anomaly_list')
        assert resolve(url).func == views.anomaly_list

    def test_anomaly_detail_url_resolves(self):
        """
        Test if the anomalies detail URL resolves to the anomaly_detail view.
        """
        url = reverse('anomaly_detail', kwargs={'pk': 1})
        assert resolve(url).func == views.anomaly_detail

    def test_anomaly_detail_url_with_invalid_pk(self):
        """
        Test if the anomalies detail URL raises a Resolver404 error with an invalid pk.
        """
        with pytest.raises(Exception):  # Replace Exception with the specific exception if known
            reverse('anomaly_detail', kwargs={'pk': 'invalid'})

    def test_index_url_reverse(self):
        """
        Test if reverse function generates correct URL for index.
        """
        url = reverse('index')
        assert url == '/'

    def test_anomaly_list_url_reverse(self):
        """
        Test if reverse function generates correct URL for anomaly_list.
        """
        url = reverse('anomaly_list')
        assert url == '/anomalies/'

    def test_anomaly_detail_url_reverse(self):
        """
        Test if reverse function generates correct URL for anomaly_detail.
        """
        url = reverse('anomaly_detail', kwargs={'pk': 1})
        assert url == '/anomalies/1/'