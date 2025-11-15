"""
Handles user interface flow.
"""
import logging
from tabulate import tabulate

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
