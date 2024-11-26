


import pytest
from pgvector.psycopg2 import register_vector
from unittest.mock import Mock, patch
from io import BytesIO

from sentence_transformers import SentenceTransformer

import config_local as config

from fonctions import *


model = SentenceTransformer('all-MiniLM-L6-v2')




####################### test reel #############################################


def test_connection_db_real():
    conn, cur = connection_db()
    assert conn is not None
    assert cur is not None
    cur.execute("SELECT 1;")  # Test simple pour vérifier la connexion
    save_and_stop_connection(conn, cur)

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
    return conn, cur
    # save_and_stop_connection(conn, cur)


# Tests de connexion
def test_connection_db():
    conn, cur = connection_db(database=TEST_DATABASE)
    assert conn is not None
    assert cur is not None
    save_and_stop_connection(conn, cur)


# Test de création de table classique 
def test_create_table(db_connection):
    conn, cur = db_connection
    create_table(TEST_TABLE, ["id", "name"], ["SERIAL PRIMARY KEY", "VARCHAR"])
    cur.execute(f"SELECT * FROM information_schema.tables WHERE table_name = '{TEST_TABLE}';")
    result = cur.fetchone()
    assert result is not None  # Vérifie que la table a été créée


# # Test de création de table vectoriel
# def test_create_table(db_connection):
#     conn, cur = db_connection
#     create_table(TEST_TABLE, ["id", "name"], ["SERIAL PRIMARY KEY", "VARCHAR"])
#     cur.execute(f"SELECT * FROM information_schema.tables WHERE table_name = '{TEST_TABLE}';")
#     result = cur.fetchone()
#     assert result is not None  # Vérifie que la table a été créée


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

@pytest.mark.find_matching
# Test de recherche dans la base vectorielle
def test_find_matching(db_connection):
    conn, cur = db_connection
    # Créer une table pour stocker des vecteurs
    if table_existance("test_vectors")=="false":
        cur.execute('CREATE EXTENSION IF NOT EXISTS vector ; ')

        cur.execute(f"""
                    CREATE TABLE test_vectors (
                        embedding VECTOR(384),
                        value VARCHAR 
                        );
                    """)
        save_and_stop_connection(conn,cur)


    assert table_existance("test_vectors")=="true"

    conn, cur = db_connection

    # Ajouter des données vectorielles fictives
    embedding = model.encode("Test document").tolist()

    

    cur.execute("INSERT INTO test_vectors (embedding, value) VALUES (%s, %s);", (embedding,"Test document"))
    conn.commit()

    assert check_consistancy("test_vectors")=="true"

    # Chercher des correspondances
    query_embedding = model.encode("Test query").tolist()
    result = find_matching(query_embedding, "test_vectors", limit=1)

    # assert len(result) == 1
    # assert result[0][1] is not None  # Vérifie que le score de similarité est présent

    # Nettoyer la table
    # cur.execute("DROP TABLE test_vectors;")
    # conn.commit()


# Test de listing des tables
def test_listing_table():
    tables = listing_table(TEST_DATABASE)
    assert TEST_TABLE not in tables.split()  


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
    assert "document vectorisé et enregistré" or "already exists" in result