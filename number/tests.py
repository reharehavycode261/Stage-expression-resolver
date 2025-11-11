from django.test import TestCase
from .models import NumberData

class AnomalyTests(TestCase):

    def test_anomaly_detection(self):
        normal_number = NumberData.objects.create(value=100)
        outlier_number = NumberData.objects.create(value=1500)

        normal_number.check_for_anomalies()
        outlier_number.check_for_anomalies()

        self.assertFalse(normal_number.detected_anomaly)
        self.assertTrue(outlier_number.detected_anomaly)
        self.assertEqual(outlier_number.anomaly_reason, "Valeur hors de la plage normale")