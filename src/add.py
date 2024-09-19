import datetime
import os
import json


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

