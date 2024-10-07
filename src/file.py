import os
import re
import json
import pyperclip
from colorama import Fore

from directory import locate_context  # Ensure this function is in directory.py


# -----------------------------------------------------------
# Function add:
# Adds a file to the current context.
# -----------------------------------------------------------
def add(file_path):
    try:
        # Get current context
        context_dir, current_context_file, context_data = get_current_context()
        if not context_data:
            print(f"No file found {current_context_file} or it is empty.")
            return

        # Get the correct path of the file to add
        global_context_dir = os.path.join(os.path.expanduser('~'), 'GPT-context', '.context')
        file_to_add = os.path.abspath(file_path) if context_dir == global_context_dir else os.path.relpath(file_path,
                                                                                                           start=os.path.dirname(
                                                                                                               context_dir))

        # Check if the file is already in the list
        if file_to_add in context_data.get('files', []):
            print(f"The file is already added: {file_path}.")
            return

        # Add the file to the list and save changes
        context_data.setdefault('files', []).append(file_to_add)
        save_json_file(current_context_file, context_data)

        print(f"{Fore.GREEN}====================> File {file_path} added correctly to current context \u2705")

    except Exception as e:
        print(f"An error occurred while adding the file: {e}")


# -----------------------------------------------------------
# Function check:
# Generates the current context (name, files, and content).
# -----------------------------------------------------------
def check():
    clipboard = ""
    try:
        # Get current context
        context_dir, current_context_file, context_data = get_current_context()
        if not context_data:
            print(f"No file found {current_context_file} or it is empty.")
            return

        # Get the name of the context
        context_name = context_data.get('name', None)
        if not context_name:
            print("The current context does not have a defined name.")
            return

        clipboard += f"Current context: {context_name}\n"

        # Concatenate the text to the variable
        clipboard += "Files in the context:\n"
        for file_name in context_data.get('files', []):
            clipboard += f"- {file_name}\n"
            try:
                # Correct path of the file
                full_path = os.path.abspath(os.path.join(os.path.dirname(context_dir), file_name))

                # Read the content of the file
                with open(full_path, 'r') as file:
                    content = file.read()

                    # Call the method to extract the delimited fragments
                    fragments = extract_fragments(content, context_name)

                    # If no fragments are found, display the full file
                    if not fragments:
                        clipboard += (
                            f"No specific fragments found for the context '{context_name}' in {file_name}. "
                            f"Displaying the full file:\n{content}\n")
                    else:
                        # Display each extracted fragment
                        for fragment in fragments:
                            clipboard += (
                                f"Fragment from {file_name} for the context '{context_name}':\n{fragment}\n")

            except Exception as e:
                print(f"Could not read file {file_name}: {e}\n")

        print(clipboard)
        pyperclip.copy(clipboard)
        print(f"{Fore.GREEN}=================================================> Context copied to clipboard \u2705")

    except Exception as e:
        print(f"An error occurred while checking the context: {e}\n")


def extract_fragments(content, context_name):
    """
    Extracts all fragments delimited by CONTEXT_<context_name>_START and CONTEXT_<context_name>_END.

    Args:
    - content: The content of the file.
    - context_name: The name of the context used to find the tags.

    Returns:
    - A list of fragments extracted between the start and end tags.
    """
    # Start and end tags
    start_tag = f"CONTEXT_{context_name}_START"
    end_tag = f"CONTEXT_{context_name}_END"

    # Find all start and end positions of the fragments
    start_positions = [match.end() for match in re.finditer(start_tag, content)]
    end_positions = [match.start() for match in re.finditer(end_tag, content)]

    # If there are no start positions, return an empty list
    if not start_positions:
        return []

    # Ensure there are enough end tags; if not, extend to the end
    if len(end_positions) < len(start_positions):
        end_positions.append(len(content))  # Add the end of the file as the last possible end

    # Extract the fragments between each pair of tags
    fragments = []
    for start_idx, end_idx in zip(start_positions, end_positions):
        fragment = content[start_idx:end_idx].strip()
        fragments.append(fragment)

    return fragments


# -----------------------------------------------------------
# Function change_context:
# Changes the current context to the specified one. Before changing,
# it saves the current context in all_context.json.
# -----------------------------------------------------------
def change_context(new_context_name):
    try:
        # Get current context
        context_dir, current_context_file, current_context = get_current_context()
        all_contexts_file = os.path.join(context_dir, 'all_context.json')
        all_contexts = load_json_file(all_contexts_file, default=[])

        # Save the current context in all_context.json
        if current_context:
            update_all_contexts(all_contexts, current_context)
            save_json_file(all_contexts_file, all_contexts)

        # Find or create the new context
        new_context = find_or_create_context(all_contexts, new_context_name)

        # Save the new context in current_context.json
        save_json_file(current_context_file, new_context)

        print(f"Changed to context '{new_context_name}'.")

    except Exception as e:
        print(f"An error occurred while changing the context: {e}")


def list():
    try:
        context_dir = locate_context()
        all_context_dir = os.path.join(context_dir, 'all_context.json')
        all_context_data = load_json_file(all_context_dir, default=[])

        # Print the listing of contexts in a custom format
        print("List of contexts:")
        for context in all_context_data:
            name = context.get('name', 'unnamed')
            files = context.get('files', [])
            files_list = ', '.join(files) if files else 'no files'
            print(f' - Context: "{name}", Content: Files: {files_list}')
    except Exception as e:
        print(f"An error occurred while listing the contexts: {e}")


# -----------------------------------------------------------
# Support functions
# -----------------------------------------------------------

def get_current_context():
    try:
        context_dir = locate_context()
        current_context_file = os.path.join(context_dir, 'current_context.json')
        context_data = load_json_file(current_context_file, default={})
        return context_dir, current_context_file, context_data
    except Exception as e:
        print(f"An error occurred while getting the current context: {e}")
        return None, None, None


def load_json_file(file_path, default):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as json_file:
                return json.load(json_file)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return default


def save_json_file(file_path, data):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        print(f"Error saving {file_path}: {e}")


def update_all_contexts(all_contexts, current_context):
    for context in all_contexts:
        if context.get("name") == current_context.get("name"):
            context.update(current_context)
            return
    all_contexts.append(current_context)


def find_or_create_context(all_contexts, new_context_name):
    for context in all_contexts:
        if context.get("name") == new_context_name:
            return context
    # If not found, create a new one
    print(f"No context found '{new_context_name}'. Creating a new one.")
    new_context = {"name": new_context_name, "files": []}
    all_contexts.append(new_context)
    return new_context


# -----------------------------------------------------------
# Testing
# -----------------------------------------------------------

if __name__ == "__main__":
    check()
    # list()
