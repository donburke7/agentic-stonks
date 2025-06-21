import os
import psycopg2


def get_db_connection():
    """
    Creating a connection to the postgres database
    :return: Connection Object
    """
    return psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'),
        database=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )