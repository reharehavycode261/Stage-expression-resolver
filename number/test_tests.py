import pytest
from django.core.exceptions import ValidationError
from .models import NumberData

@pytest.mark.django_db
class TestAnomalyDetection:
    """Test suite for anomaly detection in NumberData model."""

    def test_anomaly_detection_normal_value(self):
        """Test that a normal value does not trigger anomaly detection."""
        normal_number = NumberData.objects.create(value=100)
        normal_number.check_for_anomalies()
        assert not normal_number.detected_anomaly, "Normal value should not be detected as anomaly."

    def test_anomaly_detection_outlier_value(self):
        """Test that an outlier value triggers anomaly detection."""
        outlier_number = NumberData.objects.create(value=1500)
        outlier_number.check_for_anomalies()
        assert outlier_number.detected_anomaly, "Outlier value should be detected as anomaly."
        assert outlier_number.anomaly_reason == "Valeur hors de la plage normale", "Anomaly reason should be 'Valeur hors de la plage normale'."

    def test_anomaly_detection_edge_case_low(self):
        """Test the edge case where the value is just below the anomaly threshold."""
        edge_case_low = NumberData.objects.create(value=99)
        edge_case_low.check_for_anomalies()
        assert not edge_case_low.detected_anomaly, "Value just below threshold should not be detected as anomaly."

    def test_anomaly_detection_edge_case_high(self):
        """Test the edge case where the value is just above the anomaly threshold."""
        edge_case_high = NumberData.objects.create(value=101)
        edge_case_high.check_for_anomalies()
        assert not edge_case_high.detected_anomaly, "Value just above threshold should not be detected as anomaly."

    def test_anomaly_detection_invalid_value(self):
        """Test that invalid values raise appropriate exceptions."""
        with pytest.raises(ValidationError):
            NumberData.objects.create(value="invalid")

    def test_anomaly_detection_negative_value(self):
        """Test that negative values are handled correctly."""
        negative_number = NumberData.objects.create(value=-100)
        negative_number.check_for_anomalies()
        assert not negative_number.detected_anomaly, "Negative value should not be detected as anomaly."