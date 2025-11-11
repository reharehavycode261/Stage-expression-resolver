import pytest
from django.core.exceptions import ValidationError
from .models import Character, Anomaly

@pytest.mark.django_db
class TestAnomaly:

    def test_anomaly_creation(self):
        """Test the creation of an Anomaly instance with valid data."""
        anomaly = Anomaly.objects.create(description="Test Anomaly")
        assert anomaly.description == "Test Anomaly", "Anomaly description should match the input"
        assert not anomaly.is_resolved, "Anomaly should be unresolved by default"

    def test_anomaly_creation_empty_description(self):
        """Test the creation of an Anomaly instance with an empty description."""
        with pytest.raises(ValidationError) as excinfo:
            anomaly = Anomaly(description="")
            anomaly.full_clean()  # Trigger validation
        assert "description" in str(excinfo.value), "Validation error should occur for empty description"

@pytest.mark.django_db
class TestCharacterAnomalyAssociation:

    def test_character_anomaly_association(self):
        """Test associating an Anomaly with a Character."""
        character = Character.objects.create(name="Test Character")
        anomaly = Anomaly.objects.create(description="Test Anomaly")
        character.detected_anomalies.add(anomaly)
        assert anomaly in character.detected_anomalies.all(), "Anomaly should be associated with the character"

    def test_character_anomaly_association_no_anomalies(self):
        """Test a Character with no associated Anomalies."""
        character = Character.objects.create(name="Test Character")
        assert character.detected_anomalies.count() == 0, "Character should have no anomalies initially"

    def test_character_anomaly_association_multiple_anomalies(self):
        """Test associating multiple Anomalies with a Character."""
        character = Character.objects.create(name="Test Character")
        anomaly1 = Anomaly.objects.create(description="Test Anomaly 1")
        anomaly2 = Anomaly.objects.create(description="Test Anomaly 2")
        character.detected_anomalies.add(anomaly1, anomaly2)
        assert character.detected_anomalies.count() == 2, "Character should have two associated anomalies"
        assert anomaly1 in character.detected_anomalies.all(), "Anomaly 1 should be associated with the character"
        assert anomaly2 in character.detected_anomalies.all(), "Anomaly 2 should be associated with the character"