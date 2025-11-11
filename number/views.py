from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Character, Anomaly

def detect_anomalies(data):
    # Exemple simplifié de détection d'anomalies
    anomalies = []
    if np.mean(data) > threshold:  # Supposons qu'une valeur seuil soit définie
        anomalies.append("Mean value too high")
    return anomalies

def character_detail(request, character_id):
    character = get_object_or_404(Character, pk=character_id)
    data = []  # Supposons que nous obtenons des données à partir de `character`

    anomalies = detect_anomalies(data)
    for description in anomalies:
        anomaly, created = Anomaly.objects.get_or_create(description=description)
        character.detected_anomalies.add(anomaly)

    context = {'character': character, 'anomalies': character.detected_anomalies.all()}
    return render(request, 'character_detail.html', context)