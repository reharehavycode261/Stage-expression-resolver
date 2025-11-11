import pytest
from django.utils import timezone
from number.models import Anomaly, Character

@pytest.mark.django_db
class TestAnomalyModel:
    def test_anomaly_creation(self):
        """Test the creation of an Anomaly instance."""
        anomaly = Anomaly.objects.create(description="Test anomaly")
        assert anomaly.description == "Test anomaly"
        assert anomaly.is_resolved is False
        assert anomaly.created_at <= timezone.now()

    def test_anomaly_str_method(self):
        """Test the __str__ method of Anomaly model."""
        anomaly = Anomaly.objects.create(description="Test anomaly")
        expected_str = f"Anomaly(id={anomaly.id}, resolved={anomaly.is_resolved})"
        assert str(anomaly) == expected_str

    def test_anomaly_default_values(self):
        """Test the default values of Anomaly fields."""
        anomaly = Anomaly.objects.create(description="Test anomaly")
        assert anomaly.is_resolved is False

@pytest.mark.django_db
class TestCharacterModel:
    def test_character_creation(self):
        """Test the creation of a Character instance."""
        character = Character.objects.create(name="Test Character")
        assert character.name == "Test Character"
        assert character.detected_anomalies.count() == 0

    def test_character_anomaly_relationship(self):
        """Test the ManyToMany relationship between Character and Anomaly."""
        anomaly = Anomaly.objects.create(description="Linked anomaly")
        character = Character.objects.create(name="Test Character")
        character.detected_anomalies.add(anomaly)
        assert character.detected_anomalies.count() == 1
        assert anomaly in character.detected_anomalies.all()
        assert character in anomaly.characters.all()

    def test_character_str_method(self):
        """Test the __str__ method of Character model."""
        character = Character.objects.create(name="Test Character")
        assert str(character) == character.name

    def test_character_anomaly_removal(self):
        """Test removal of an Anomaly from a Character."""
        anomaly = Anomaly.objects.create(description="Removable anomaly")
        character = Character.objects.create(name="Test Character")
        character.detected_anomalies.add(anomaly)
        character.detected_anomalies.remove(anomaly)
        assert character.detected_anomalies.count() == 0
        assert anomaly not in character.detected_anomalies.all()