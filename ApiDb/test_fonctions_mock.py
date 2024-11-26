import pytest
from pgvector.psycopg2 import register_vector
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
