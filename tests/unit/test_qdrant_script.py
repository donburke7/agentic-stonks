import pytest
from qdrant_client.http.models import Distance, VectorParams
from scripts.qdrant_script import QdrantWorker


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("QDRANT_URL", "http://fake-url:6333")

@pytest.fixture
def mock_pg(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_conn.cursor.return_value = mock_cursor
    mocker.patch("scripts.qdrant_script.get_db_connection", return_value=mock_conn)
    return mock_conn, mock_cursor

@pytest.fixture
def mock_qdrant(mocker):
    return mocker.patch("scripts.qdrant_script.QdrantClient")

def test_create_collection_if_not_exists(mock_env, mock_pg, mock_qdrant):
    mock_conn, mock_cursor = mock_pg
    mock_client_instance = mock_qdrant.return_value
    mock_client_instance.collection_exists.return_value = False

    worker = QdrantWorker(collection_name="test_collection")
    worker.create_collection()

    mock_client_instance.collection_exists.assert_called_once_with(collection_name="test_collection")
    mock_client_instance.create_collection.assert_called_once_with(
        collection_name="test_collection",
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
    )
    worker.close()

def test_create_collection_if_exists(mock_env, mock_pg, mock_qdrant):
    mock_client_instance = mock_qdrant.return_value
    mock_client_instance.collection_exists.return_value = True

    worker = QdrantWorker(collection_name="test_collection")
    worker.create_collection()

    mock_client_instance.create_collection.assert_not_called()
    worker.close()

def test_reset_collection(mock_env, mock_pg, mock_qdrant):
    mock_client_instance = mock_qdrant.return_value
    mock_client_instance.collection_exists.return_value = True

    worker = QdrantWorker(collection_name="test_collection")
    worker.reset_collection()

    mock_client_instance.delete_collection.assert_called_once_with(collection_name="test_collection")
    mock_client_instance.create_collection.assert_called_once_with(
        collection_name="test_collection",
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
    )
    worker.close()

def test_reset_collection_when_does_not_exist(mock_env, mock_pg, mock_qdrant):
    mock_client_instance = mock_qdrant.return_value
    mock_client_instance.collection_exists.return_value = False

    worker = QdrantWorker(collection_name="test_collection")
    worker.reset_collection()

    mock_client_instance.delete_collection.assert_not_called()
    mock_client_instance.create_collection.assert_not_called()
    worker.close()
