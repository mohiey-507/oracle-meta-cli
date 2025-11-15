"""
Handles database connection.
"""

import logging
import oracledb

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
