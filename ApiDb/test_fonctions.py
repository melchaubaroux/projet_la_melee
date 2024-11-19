


import pytest
import psycopg2
from unittest.mock import Mock, patch
from io import BytesIO

from sentence_transformers import SentenceTransformer

import config_local as config

from fonctions import *


model = SentenceTransformer('all-MiniLM-L6-v2')


# Fixtures for setup and teardown
@pytest.fixture
def mock_connection():
    """Fixture to mock database connection and cursor."""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor

# Tests for database connection
def test_connection_db(mock_connection):
    with patch('fonctions.psycopg2.connect', return_value=mock_connection[0]):
        conn, cur = connection_db()
        assert conn is not None
        assert cur is not None

def test_connection_db_real():
    conn, cur = connection_db()
    assert conn is not None
    assert cur is not None
    cur.execute("SELECT 1;")  # Test simple pour vérifier la connexion
    save_and_stop_connection(conn, cur)


def test_save_and_stop_connection(mock_connection):
    conn, cur = mock_connection
    save_and_stop_connection(conn, cur)
    conn.commit.assert_called_once()
    cur.close.assert_called_once()
    conn.close.assert_called_once()

def test_drop_table(mock_connection):
    _, cur = mock_connection
    drop_table("test_table", cur)
    cur.execute.assert_called_with("DROP TABLE test_table ;")

def test_table_existance(mock_connection):
    conn, cur = mock_connection
    with patch('fonctions.connection_db', return_value=(conn, cur)):
        cur.fetchone.return_value = ["column_name"]
        result = table_existance("test_table")
        assert result == "true"

# Tests for utility functions
def test_extension_file_suppression():
    result = extension_file_suppression("document.pdf")
    assert result == "document"

def test_query_vectorisation():
    query = "This is a test query."
    result = query_vectorisation(query)
    assert isinstance(result, list)
    assert len(result) > 0

def test_document_vectorisation(mock_connection):
    file = Mock()
    file.filename = "test.txt"
    file.file = BytesIO(b"This is a test document.")
    with patch('fonctions.connection_db', return_value=mock_connection), \
         patch('fonctions.register_vector'), \
         patch('fonctions.remove') as mock_remove:
        document_vectorisation(file)
        mock_remove.assert_called_once_with("test")

# Tests for find_matching
def test_find_matching(mock_connection):
    conn, cur = mock_connection
    with patch('fonctions.connection_db', return_value=(conn, cur)):
        cur.fetchall.return_value = [("result1", 0.5), ("result2", 0.7)]
        result = find_matching([0.1, 0.2, 0.3], "test_table", limit=2)
        assert len(result) == 2
        assert result[0][0] == "result1"

# Tests for extract_document_informations
def test_extract_document_informations(mock_connection):
    with patch('fonctions.find_matching', return_value=[("doc", 0.5)]):
        documents = [("doc1",), ("doc2",)]
        result = extract_document_informations(documents, [0.1, 0.2, 0.3])
        assert len(result) > 0


# Configuration pour les tests (remplacez par vos valeurs)
TEST_DATABASE =  config.database
TEST_USER =config.user
TEST_PASSWORD = config.password
TEST_HOST = config.host
TEST_TABLE = "test_table"

@pytest.fixture(scope="module")
def db_connection():
    """
    Fixture pour gérer une connexion réelle à une base de données.
    """
    conn, cur = connection_db(database=TEST_DATABASE)
    yield conn, cur
    save_and_stop_connection(conn, cur)


# Tests de connexion
def test_connection_db():
    conn, cur = connection_db(database=TEST_DATABASE)
    assert conn is not None
    assert cur is not None
    save_and_stop_connection(conn, cur)


# Test de création de table
def test_create_table(db_connection):
    conn, cur = db_connection
    create_table(TEST_TABLE, ["id", "name"], ["SERIAL PRIMARY KEY", "VARCHAR"])
    cur.execute(f"SELECT * FROM information_schema.tables WHERE table_name = '{TEST_TABLE}';")
    result = cur.fetchone()
    assert result is not None  # Vérifie que la table a été créée


# Test de vérification d'existence de table
def test_table_existance():
    result = table_existance(TEST_TABLE)
    assert result == "true"


# Test d'insertion de données
def test_insert_many(db_connection):
    conn, cur = db_connection
    create_table(TEST_TABLE, ["id", "name"], ["SERIAL PRIMARY KEY", "VARCHAR"])
    insert_many(TEST_TABLE, ["id", "name"], [(1, "Alice"), (2, "Bob")])

    cur.execute(f"SELECT * FROM {TEST_TABLE};")
    results = cur.fetchall()
    assert len(results) == 2
    assert results[0][1] == "Alice"
    assert results[1][1] == "Bob"


# Test de récupération des données
def test_get_table(db_connection):
    conn, cur = db_connection
    data = get_table(TEST_TABLE)
    assert len(data) == 2  # Correspond à l'insertion précédente
    assert data[0][1] == "Alice"
    assert data[1][1] == "Bob"


# Test de suppression de table
def test_drop_table(db_connection):
    conn, cur = db_connection
    drop_table(TEST_TABLE, cur)
    cur.execute(f"SELECT * FROM information_schema.tables WHERE table_name = '{TEST_TABLE}';")
    result = cur.fetchone()
    assert result is None  # Vérifie que la table a été supprimée


# Test de vectorisation de requête
def test_query_vectorisation():
    query = "This is a test query."
    vector = query_vectorisation(query)
    assert isinstance(vector, list)
    assert len(vector) > 0


# Test de suppression d'extension de fichier
def test_extension_file_suppression():
    result = extension_file_suppression("document.pdf")
    assert result == "document"


# Test de recherche dans la base vectorielle
def test_find_matching(db_connection):
    conn, cur = db_connection
    # Créer une table pour stocker des vecteurs
    if table_existance("test_vectors")=="false":
        cur.execute("CREATE TABLE IF NOT EXISTS test_vectors (id SERIAL PRIMARY KEY, embedding VECTOR(384), value VARCHAR);")
        conn.commit()

    assert table_existance("test_vectors")=="true"

    # Ajouter des données vectorielles fictives
    
    embedding = model.encode("Test document").tolist()

    

    cur.execute("INSERT INTO test_vectors (embedding, value) VALUES (%s, %s);", (embedding, "Test document"))
    conn.commit()

    assert check_consistancy(TEST_TABLE)=="true"

    # Chercher des correspondances
    query_embedding = model.encode("Test query").tolist()
    result = find_matching(query_embedding, "test_vectors", limit=1)

    assert len(result) == 1
    assert result[0][1] is not None  # Vérifie que le score de similarité est présent

    # Nettoyer la table
    cur.execute("DROP TABLE test_vectors;")
    conn.commit()


# Test de listing des tables
def test_listing_table():
    tables = listing_table(TEST_DATABASE)
    assert TEST_TABLE not in tables.split()  # Car elle a été supprimée après les tests précédents


# Test de vectorisation de document
def test_document_vectorisation(db_connection):
    conn, cur = db_connection
    # Simuler un fichier
    from io import BytesIO
    file = Mock()
    file.filename = "test_document.txt"
    file.file = BytesIO(b"This is a test document.")

    if table_existance("test_document")=="true":
        drop_table("test_document")

    result = document_vectorisation(file)
    assert "document vectorisé et enregistré" in result