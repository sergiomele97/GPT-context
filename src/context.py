import datetime
import os
import argparse
import json


def init_context_repo():
    """Initializes a new context repository in the current directory."""
    repo_path = os.getcwd()  # Use the current directory
    context_dir = os.path.join(repo_path, '.context')

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


def add_context(prompt, response):
    """Adds a new context to the repository."""
    repo_path = os.getcwd()  # Use the current directory
    context_dir = os.path.join(repo_path, '.context')
    context_file = os.path.join(context_dir, 'context.json')

    try:
        if not os.path.exists(context_dir):
            raise FileNotFoundError(f"The context directory does not exist in {context_dir}")

        with open(context_file, 'r') as f:
            context_data = json.load(f)

        context_data.append({
            "name": f"Prompt {len(context_data) + 1}",
            "prompt": prompt,
            "response": response,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        with open(context_file, 'w') as f:
            json.dump(context_data, f, indent=4)

        print(f"Context added to {context_file}.")
    except Exception as e:
        print(f"Error adding context: {e}")


def main():
    parser = argparse.ArgumentParser(description="Context management tool.")
    subparsers = parser.add_subparsers(dest='command')

    # Command 'init'
    subparsers.add_parser('init', help='Initialize a new context repository.')

    # Command 'add'
    add_parser = subparsers.add_parser('add', help='Add a new context to the repository.')
    add_parser.add_argument('prompt', help='The prompt for the context.')
    add_parser.add_argument('response', help='The response for the context.')

    args = parser.parse_args()

    if args.command == 'init':
        init_context_repo()
    elif args.command == 'add':
        add_context(args.prompt, args.response)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
