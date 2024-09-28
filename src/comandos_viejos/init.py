import os
import json
from src.comandos_viejos import directory


def init_context_repo():
    """Initializes a new context repository in the nearest .context directory or in the current directory."""
    # Find the .context directory
    context_dir = directory.find_context_repo(os.getcwd())

    if context_dir is None:
        # No .context directory found, create one in the current directory
        context_dir = os.path.join(os.getcwd(), '.context')

    if os.path.exists(context_dir):
        print(f"The context repository already exists in {context_dir}.")
        return

    try:
        # Create the repository directory and subdirectories
        os.makedirs(context_dir, exist_ok=True)

        # Create the context file with an initial empty list
        context_file = os.path.join(context_dir, 'context.json')
        with open(context_file, 'w') as f:
            json.dump([], f)

        print(f"Context repository initialized in {context_dir}.")
    except Exception as e:
        print(f"Error initializing repository: {e}")


if __name__ == "__main__":
    init_context_repo()