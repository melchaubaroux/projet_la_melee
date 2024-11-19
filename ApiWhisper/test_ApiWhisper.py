import os
import pytest
import httpx
from fastapi.testclient import TestClient
from ApiWhisper import app  # Assurez-vous d'importer l'application FastAPI depuis votre module.
from unittest.mock import patch

# Configuration du client pour tester l'API
client = TestClient(app)

# Test de l'endpoint /transcription avec un fichier audio simulé
@pytest.mark.asyncio
@patch("send_email.send_email") 
async def test_transcription(mock_send_email):
    # Préparer un fichier audio simulé
    audio_file_path = "test_audio.mp3"
    
    # Assurez-vous que le fichier audio de test existe. Vous pouvez aussi utiliser un fichier audio réel ou simulé.
    if not os.path.exists(audio_file_path):
        # Créez un fichier audio temporaire pour les tests
        with open(audio_file_path, "wb") as f:
            f.write(b"Test audio content")  # Simule le contenu d'un fichier audio.

    # Ouvrir le fichier pour l'envoyer dans la requête POST
    with open(audio_file_path, "rb") as f:
        response = client.post(
            "/transcription", 
            files={"file": ("test_audio.mp3", f, "audio/mpeg")},
            params={"sender": "mel.chaubaroux@gmail.com", "recipients": "mel.chaubaroux@gmail.com"}
        )

    
    # Vérifier si la fonction d'envoi d'email a bien été appelée
    mock_send_email.assert_called_once_with(
        subject="transcription audio de test_audio.mp3",
        text=response.text,
        sender="mel.chaubaroux@gmail.com",
        recipients="mel.chaubaroux@gmail.com"
    )
        
    # Vérifier que la réponse est correcte
    assert response.status_code == 200
    assert "transcription audio de test_audio" in response.text  # Vérifie que le sujet du mail est correct.
    
    # Vérifier si le texte de transcription contient un résultat.
    assert len(response.text) > 0

    # Nettoyer le fichier de test après le test
    if os.path.exists(audio_file_path):
        os.remove(audio_file_path)


# Test de l'API /transcription pour vérifier l'email envoyé (mock de l'email)
@pytest.mark.asyncio
@patch("send_email.send_email")  # Mock la fonction d'envoi d'email pour éviter un email réel
async def test_transcription_email(mock_send_email):
    audio_file_path = "test_audio.mp3"

    # Créer un fichier audio simulé pour les tests
    if not os.path.exists(audio_file_path):
        with open(audio_file_path, "wb") as f:
            f.write(b"Test audio content")  # Simule le contenu du fichier audio.

    # Effectuer la requête POST avec un fichier audio
    with open(audio_file_path, "rb") as f:
        response = await client.post(
            "/transcription",
            files={"file": ("test_audio.mp3", f, "audio/mpeg")},
            params={"sender": "mel.chaubaroux@gmail.com", "recipients": "mel.chaubaroux@gmail.com"}
        )

    # Vérifier que la réponse a le bon statut HTTP
    assert response.status_code == 200
    assert "transcription audio de test_audio" in response.text

    # Vérifier si la fonction d'envoi d'email a bien été appelée
    mock_send_email.assert_called_once_with(
        subject="transcription audio de test_audio.mp3",
        text=response.text,
        sender="mel.chaubaroux@gmail.com",
        recipients="mel.chaubaroux@gmail.com"
    )

    # Nettoyer le fichier de test après
    if os.path.exists(audio_file_path):
        os.remove(audio_file_path)
