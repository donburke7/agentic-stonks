import os
from db.utils import get_db_connection
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, models


class QdrantWorker:
    def __init__(self):
        self.pg_conn = get_db_connection()
        self.pg_cur = self.pg_conn.cursor()
        self.qdrant_client = QdrantClient(url=os.environ["QDRANT_URL"])
        self.collection_name = "sec_articles"

    def create_collection(self):
        """
        Creates a collection in the Qdrant database if it does not already exist.

        :raises QdrantClientException: If there is an error while creating or
            verifying the existence of the collection.
        """
        if not self.qdrant_client.collection_exists(collection_name=self.collection_name):
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                # Adjust vector size based on embeddings
                vectors_config=VectorParams(size=1536, distance=models.Distance.COSINE),
            )

    def insert_into_qdrant(self):
        # INSERT CODE TO READ POSTGRES WHERE EMBEDDING IS NOT NULL, AND PUSH TO QDRANT DB
        pass


    def reset_collection(self):
        """
        Resets the specified collection in the Qdrant database by deleting it if it exists and recreating it
        with a new configuration.

        :param self: An instance of the class that manages the Qdrant client and collection.
        :raises Exception: If there is an issue during the deletion or creation process of the collection.
        :return: None
        """
        if self.qdrant_client.collection_exists(collection_name=self.collection_name):
            self.qdrant_client.delete_collection(collection_name=self.collection_name)
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                # Adjust vector size based on embeddings
                vectors_config=VectorParams(size=1536, distance=models.Distance.COSINE),
            )

    def close(self):
        self.pg_cur.close()
        self.pg_conn.close()