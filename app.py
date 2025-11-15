"""
Main.
"""
import getpass
import argparse
import logging
from db_connection import init_connection_pool, close_connection_pool

def setup_logging():
    """Sets up the logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )

def main():
    """Main application loop."""
    setup_logging()
    logging.info("Application starting.")

    parser = argparse.ArgumentParser(description='Oracle Metadata Explorer')
    parser.add_argument('--hostname', default='localhost', help="Database hostname (default 'localhost')")
    parser.add_argument('--port', default='1521', help="Database port (default '1521')")
    parser.add_argument('--service', help="Database service name (default 'ORCLPDB1')")
    args = parser.parse_args()

    print("Welcome to Oracle Metadata Explorer!")
    print("-----------------------------------")

    hostname = args.hostname or input("Enter host name (default 'localhost'): ") or "localhost"
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    service  = args.service  or input("Enter service name (default 'ORCLPDB1'): ") or "ORCLPDB1"
    dsn = f"{hostname}:{args.port}/{service}"

    if not init_connection_pool(username, password, dsn):
        logging.error("Failed to initialize database connection pool. Exiting.")
        return

    logging.info("Database connection pool initialized successfully.")

    return None

if __name__ == '__main__':
    main()
