import os
import json
from colorama import Fore

from contextignore import create_contextignore


# -----------------------------------------------------------
# init function:
# Initializes the context by creating a .context folder and a
# context.json file with information about custom contexts.
# If the folder already exists, the user will be informed and
# no further changes will be made.
# -----------------------------------------------------------
def init(target_directory):
    try:
        # Logic to initialize the context
        print("Initializing context...")

        # Define the path for the .context folder and the context.json file
        context_dir = os.path.join(target_directory, '.context')
        json_all_file_path = os.path.join(context_dir, 'all_context.json')
        json_current_file_path = os.path.join(context_dir, 'current_context.json')
        contextignore_path = os.path.join(context_dir, '.contextignore')

        # Check if the .context folder already exists
        if os.path.exists(context_dir):
            print(f"The folder '.context' already exists at: {context_dir}")
        else:
            # Create the .context folder if it doesn't exist
            os.makedirs(context_dir)
            create_json(json_all_file_path, 0)
            create_json(json_current_file_path, 1)
            create_contextignore(contextignore_path)

            print(f"{Fore.GREEN}Context initialized. Folder created at: {context_dir}")
            print(f"{Fore.GREEN}JSON file created at: {json_all_file_path}")
            print(f"{Fore.GREEN}JSON file created at: {json_current_file_path}")
            print(f"{Fore.GREEN}File .contextignore created at: {contextignore_path}")

    except Exception as e:
        print(f"An error occurred while initializing the context: {e}")


# -----------------------------------------------------------
# locate_context function:
# Searches for the .context folder in the current directory and its
# parent directories. If it is not found, it searches in the global
# folder C:\Program Files\GPT-context. Creates the global folder if
# it doesn't exist and returns the corresponding path.
# -----------------------------------------------------------
def locate_context():
    # Define the global path where the default context should be
    global_context_dir = os.path.join(os.path.expanduser('~'), '.context')

    # Start from the current directory
    current_dir = os.getcwd()

    while True:
        # Define the path for the .context folder in the current directory
        context_dir = os.path.join(current_dir, '.context')

        try:
            # Check if the .context folder exists in the current directory
            if os.path.exists(context_dir):
                print(f"Local context found at: {context_dir}")
                return context_dir
        except Exception as e:
            print(f"An error occurred while checking the local context: {e}")
            return None  # Return None to indicate failure

        # Move up one level in the parent directory
        parent_dir = os.path.dirname(current_dir)

        # If we have reached the root directory, exit the loop
        if parent_dir == current_dir:
            break

        current_dir = parent_dir

    # If no local context was found, check the global context
    try:
        if not os.path.exists(global_context_dir):
            init(os.path.expanduser('~'))

    except Exception as e:
        print(f"An error occurred while creating the global context: {e}")

    print(f"Using global context at: {global_context_dir}")
    return global_context_dir


# -----------------------------------------------------------
# create_json function:
# Creates a standard context.json file inside the .context folder
# -----------------------------------------------------------
def create_json(json_file_path, context_number):
    # Define different contexts based on the number
    if context_number == 1:
        context_data = \
        {
            "name": "default",
            "files":
                [
                ]
        }
    else:
        # Default value: A list of context objects
        context_data =  [
        {
            "name": "default",
            "files":
                [
                ]
        }
    ]

    # Save the contexts to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(context_data, json_file, indent=4)


# -----------------------------------------------------------
# Testing
# -----------------------------------------------------------
if __name__ == "__main__":
    init(os.getcwd())
    locate_context()
