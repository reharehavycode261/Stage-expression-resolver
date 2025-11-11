from django.test import TestCase
from .models import Character, Anomaly

class AnomalyTests(TestCase):
    
    def test_anomaly_creation(self):
        anomaly = Anomaly.objects.create(description="Test Anomaly")
        self.assertEqual(anomaly.description, "Test Anomaly")
        self.assertFalse(anomaly.is_resolved)
    
    def test_character_anomaly_association(self):
        character = Character.objects.create(name="Test Character")
        anomaly = Anomaly.objects.create(description="Test Anomaly")
        character.detected_anomalies.add(anomaly)
        self.assertIn(anomaly, character.detected_anomalies.all())