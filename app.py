"""
Main.
"""
import getpass
import argparse
import logging
from db_connection import init_connection_pool, close_connection_pool
from ui_flow import handle_main_menu, handle_object_list, handle_object_details

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

    state_handlers = {
        'main_menu': handle_main_menu,
        'object_list': handle_object_list,
        'object_details': handle_object_details,
    }

    state = 'main_menu'
    context = {}
    breadcrumb = ['[Main Menu]']

    while state != 'exit':
        logging.info(f"State: {state}, Context: {context}")
        handler = state_handlers[state]

        if state == 'main_menu':
            state, object_type = handler(breadcrumb)
            if state == 'object_list':
                context['object_type'] = object_type
        elif state == 'object_list':
            state, object_name = handler(context['object_type'], breadcrumb)
            if state == 'object_details':
                context['object_name'] = object_name
            elif state == 'main_menu':
                context.pop('object_type', None)
        elif state == 'object_details':
            state, returned_context = handler(context['object_type'], context['object_name'], breadcrumb)
            if state == 'object_list':
                context.pop('object_name', None)

    close_connection_pool()
    logging.info("Application shutting down.")
    print("Exiting Oracle Metadata Explorer. Goodbye!")

if __name__ == '__main__':
    main()
