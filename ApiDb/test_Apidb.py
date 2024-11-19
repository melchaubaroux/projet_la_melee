import pytest
from fastapi.testclient import TestClient
from Apidb import app # Importer votre application FastAPI
import uvicorn
import config_local as config

client = TestClient(app)  # Création d'un client de test pour interagir avec l'API




# Test de la connexion à la base de données
def test_available_connection():
    response = client.get("/available_connection")
    assert response.status_code == 200
    assert response.text in ["True", "False"]  # Connexion réussie ou échouée


# Test du monitoring
def test_monitoring():
    response = client.get("/monitoring")
    assert response.status_code == 200
    assert "cpu utilisé" in response.text  # Vérifie que le texte attendu est présent
    assert "memoire utiliser" in response.text


# Test de la vérification des autorisations
def test_verification_of_authorisation():
    username = config.user
    password = config.password
    response = client.get(f"/verification_of_authorisation?username={username}&password={password}")
    assert response.status_code == 200
    assert response.text in ["loged", "login error"]  # Vérifie que l'utilisateur est logué ou non


# Test de l'existence d'une table
def test_table_existance():
    table_name = "index"  # Nom de table à vérifier
    response = client.get(f"/exist/{table_name}")
    assert response.status_code == 200
    assert response.text in ["true", "false"]  # Table existe ou non


# Test de la liste des tables
def test_list_of_table():
    response = client.get("/list_of_table")
    assert response.status_code == 200
    assert "Bases de données disponibles:" in response.text


# Test de la récupération de toutes les données d'une table
def test_pull_all():
    table_name = "index"  # Nom de table
    response = client.get(f"/pull_all/{table_name}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Vérifie que la réponse est une liste de données


# Test de la consistance d'une table
def test_check_consistency():
    table_name = "index"
    response = client.get(f"/check_consitancy?table={table_name}")
    assert response.status_code == 200
    assert response.text[1:-1] in ["true", "false", "no table at this name"]


# Test du reset de la base de données
def test_reset_database():
    response = client.get("/reset")
    assert response.status_code == 200
    assert "index" in client.get("/list_of_table").text  # Vérifie que la table `index` a été recréée


# Test de l'upload de fichiers
def test_upload():
    file_content = b"This is a test document."
    file = {"file": ("test_document.txt", file_content)}
    response = client.post("/upload", files=file)
    assert response.status_code == 200
    assert "document vectorisé et enregistré" in response.text


# Test de la suppression de documents
def test_document_deletion():
    table_name = "test_document"
    response = client.post("/document deletion",  table_name)
    assert response.status_code == 200
    assert "no more table at this name" in client.get(f"/exist/{table_name}").text


# Test de la recherche vectorielle
def test_vectorial_search():
    query = "test query"
    response = client.post("/vectorial_search", json={"query": query, "number_of_document": 1})
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Vérifie que la réponse est une liste


# Test de la mise à jour de fichiers (endpoint encore à implémenter)
@pytest.mark.skip(reason="Endpoint /maj n'est pas encore implémenté.")
def test_update_file():
    file_content = b"Updated content."
    file = {"file": ("updated_document.txt", file_content)}
    response = client.post("/maj", files=file)
    assert response.status_code == 200
