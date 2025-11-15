"""
Handles user interface flow.
"""
import logging
from tabulate import tabulate
from config import METADATA_QUERIES
from db_connection import list_objects, get_metadata

logger = logging.getLogger(__name__)

def print_breadcrumb(breadcrumb):
    """Prints the breadcrumb trail."""
    print(' → '.join(breadcrumb))

def print_separator():
    """Prints a separator line."""
    print("\n" + "=" * 40)

def print_table(headers, data):
    """Prints data in a table format."""
    if data:
        print(tabulate(data, headers=[h.upper() for h in headers], tablefmt='grid'))
    else:
        print("No data found.")

def get_choice(prompt, valid_choices, allow_back=True):
    """Gets a valid choice from the user."""
    if allow_back:
        prompt += " (or 'b' for back): "
    while True:
        choice = input(prompt).strip().lower()
        logger.debug(f"User input: '{choice}'")
        if allow_back and choice == 'b':
            return 'back'
        if choice in valid_choices:
            return choice
        print("Invalid choice. Please try again.")

def handle_main_menu(breadcrumb):
    """Handles the main menu."""
    print_separator()
    print_breadcrumb(breadcrumb)
    print("Select the object type to view:")
    object_types = list(METADATA_QUERIES.keys())
    for i, obj_type in enumerate(object_types, 1):
        print(f"{i}. {obj_type.capitalize()}")
    print(f"{len(object_types) + 1}. Exit")
    
    choice = get_choice("Enter option number: ", [str(i) for i in range(1, len(object_types) + 2)], allow_back=False)
    if choice == str(len(object_types) + 1):
        logger.info("User chose to exit from the main menu.")
        return 'exit', None

    selected_type = object_types[int(choice) - 1]
    logger.info(f"User selected object type: {selected_type}")
    breadcrumb.append(f'[{selected_type.capitalize()}]')
    return 'object_list', selected_type

def handle_object_list(object_type, breadcrumb):
    """Handles the object list menu."""
    print_separator()
    print_breadcrumb(breadcrumb)
    objects = list_objects(object_type)
    if not objects:
        print(f"No {object_type.lower()}s found.")
        breadcrumb.pop()
        return 'main_menu', None

    print(f"Available {object_type.capitalize()}s:")
    for i, obj in enumerate(objects, 1):
        print(f"{i:2d}. {obj}")

    choice = get_choice("Select a number", [str(i) for i in range(1, len(objects) + 1)])
    if choice == 'back':
        logger.info("User chose to go back to the main menu.")
        breadcrumb.pop()
        return 'main_menu', None

    selected_object = objects[int(choice) - 1]
    logger.info(f"User selected object: {selected_object}")
    breadcrumb.append(f'[{selected_object}]')
    return 'object_details', selected_object

def handle_object_details(object_type, object_name, breadcrumb):
    """Handles the object details menu."""
    raise NotImplementedError()