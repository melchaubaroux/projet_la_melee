import os
import pytest
import httpx
from fastapi.testclient import TestClient
from ApiWhisper import app  # Assurez-vous d'importer l'application FastAPI depuis votre module.
from unittest.mock import patch
from io import BytesIO
import shutil
from param import API_KEY, EMAIL , SERVER

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

        file_content = BytesIO(f.read())
        response = client.post(
            "/transcription", 
            files={"file": ("test_audio.mp3", file_content, "audio/mpeg")},
            params={"sender":EMAIL, "recipients": EMAIL,"smtp_server":SERVER}

        )


    # Vérifier que la réponse est correcte
    assert response.status_code == 200
   
    
    # Vérifier si le texte de transcription contient un résultat.
    assert len(response.text) > 0

    #  Supprimer le dossier et son contenu après le test
    # dossier = "/test_audio"
    # shutil.rmtree(dossier)


