import os
import sys

def find_context_repo(start_path):
    """Find the nearest .context directory starting from start_path and moving up the directory tree."""
    current_path = start_path

    while current_path != os.path.dirname(current_path):  # Stop when reaching the root
        context_path = os.path.join(current_path, '.context')
        if os.path.isdir(context_path):
            return context_path
        current_path = os.path.dirname(current_path)

    return None

def context_not_found(start_path):
    print(f".context directory not found starting from {start_path}")

    print("\nUse 'context init' to initialize a context repository")

    sys.exit(0)