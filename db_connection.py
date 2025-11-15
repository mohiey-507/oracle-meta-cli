"""
Handles database connection and data retrieval.
"""

import logging
import oracledb
from .config import METADATA_QUERIES, OBJECT_LIST_QUERIES

pool = None
logger = logging.getLogger(__name__)

def init_connection_pool(username, password, dsn):
    """Initializes the database connection pool."""
    global pool
    try:
        pool = oracledb.create_pool(user=username, password=password, dsn=dsn, min=2, max=5, increment=1)
        return True
    except oracledb.Error as e:
        logger.error(f"Connection failed: {e}")
        return False

def close_connection_pool():
    """Closes the database connection pool."""
    global pool
    if pool:
        pool.close()
        pool = None
        logger.info("Database connection pool closed.")

def get_metadata(object_type, object_name, metadata_type):
    """Fetches metadata for a given database object."""
    global pool
    if not pool:
        raise ConnectionError("Connection pool is not initialized.")

    query = METADATA_QUERIES.get(object_type, {}).get(metadata_type)
    if not query:
        logger.warning(f"No metadata query found for {object_type} - {metadata_type}")
        return None, None

    logger.info(f"Fetching metadata for {object_type} '{object_name}' ({metadata_type})")
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(query, object_name=object_name)
                columns = [desc[0] for desc in cursor.description]
                return columns, cursor.fetchall()
            except oracledb.Error as e:
                logger.error(f"Error fetching metadata: {e}")
                return None, None

def list_objects(object_type):
    """Lists all objects of a given type."""
    global pool
    if not pool:
        raise ConnectionError("Connection pool is not initialized.")

    query = OBJECT_LIST_QUERIES.get(object_type)
    if not query:
        logger.warning(f"No object list query found for {object_type}")
        return []

    logger.info(f"Listing objects of type {object_type}")
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(query)
                return sorted([row[0] for row in cursor.fetchall()])
            except oracledb.Error as e:
                logger.error(f"Error listing objects: {e}")
                return []
