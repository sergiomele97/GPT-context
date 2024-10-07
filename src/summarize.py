import fnmatch
import os
import pyperclip
from colorama import init, Fore

import language
from directory import locate_context


# Read files
def read_contextignore():
    contextignore_path = os.path.join(locate_context(), '.contextignore')
    ignore_patterns = []

    try:
        # Read the .contextignore file if it exists
        if os.path.exists(contextignore_path):
            with open(contextignore_path, 'r', encoding='utf-8') as f:
                ignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except Exception as e:
        print(f"Error reading .contextignore file: {e}")

    return ignore_patterns


def should_ignore(file_path, ignore_patterns):
    """Checks if the file should be ignored based on the provided patterns."""
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False


def read_code_files(directory):
    """Reads code files in the directory, ignoring folders and files according to the patterns in .contextignore."""
    code_files = []
    ignore_patterns = read_contextignore()

    # Extract the directories to ignore from the ignore_patterns file
    ignored_directories = set(pattern.strip('/') for pattern in ignore_patterns if pattern.endswith('/'))

    for root, dirs, files in os.walk(directory):
        # Modify the list of directories to remove those matching ignored patterns
        dirs[:] = [d for d in dirs if d not in ignored_directories]

        for file in files:
            file_path = os.path.join(root, file)

            # Ignore if it matches any pattern
            if should_ignore(file_path, ignore_patterns):
                continue

            # Check if it is a code file
            if file.endswith(('.py', '.js', '.java', '.php', '.cs', '.cpp', '.c++', '.c',
                              '.rb', '.swift', '.ts', '.go', '.r', '.kt', '.pl', '.rs')):
                # Handle possible UTF-8 encoding errors
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code_files.append((file_path, f.read()))
                except UnicodeDecodeError as e:
                    print(f"File ignored due to decoding error in {file_path}: {e}")
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
    return code_files


def generate_summary(code_files):
    summary = []
    current_dir = os.getcwd()

    for file_path, code in code_files:
        try:
            # Convert the absolute path to a relative path based on the current directory
            relative_path = os.path.relpath(file_path, current_dir)

            # Attempt to extract imports, classes, and functions from the file
            imports, classes, functions = language.extract_info(file_path, code)

        except Exception as e:
            # Handle the exception, logging the error but allowing the process to continue
            print(f"Error processing {file_path}: {e}")
            continue  # Move to the next file instead of stopping execution

        # If everything is fine, add the results to the summary
        summary.append((relative_path, imports, classes, functions))

    return summary


def generate_project_context(directory):
    init(autoreset=True)
    context = ""
    print(f"Generating context for the project from directory {directory}\n")
    print(f"(If this takes too long, it may be analyzing a module or virtual environment folder by mistake. Try excluding heavy directories or add them to .contextignore (directory .context))\n\n")

    try:
        code_files = read_code_files(directory)
        summary = generate_summary(code_files)

        context = f"### Project Context located at: {os.getcwd()}\n"
        context += f"**Here is the project's file structure with its relative path, imports, classes, and functions (parameters) -> outputs:**\n\n"

        for file_path, imports, classes, functions in summary:
            context_line = f"{file_path}: "
            try:
                # Add imports
                if imports:
                    context_line += f"Imports: {', '.join(imports)}; "

                # Add classes and functions
                for class_name, class_functions in classes.items():
                    context_line += f"Class {class_name}: "
                    func_lines = []
                    for func in class_functions:
                        # Asegúrate de que func['name'], func['params'], y func['return'] no sean None
                        if func and isinstance(func, dict):
                            params = ', '.join(func['params']) if func.get('params') else 'no parameters'
                            func_lines.append(f"{func['name']}({params}) -> {func.get('return', 'no return')}")

                    functions_line = '; '.join(func_lines)
                    context_line += f"{functions_line}; "

                # Add functions that do not belong to any class
                if functions:
                    func_lines = []
                    for func in functions:
                        # Asegúrate de que func['name'], func['params'], y func['return'] no sean None
                        if func and isinstance(func, dict):
                            params = ', '.join(func['params']) if func.get('params') else 'no parameters'
                            func_lines.append(f"{func['name']}({params}) -> {func.get('return', 'no return')}")

                    functions_line = '; '.join(func_lines)
                    context_line += f"No class: {functions_line}; "

                # Remove the last "; " and add a new line
                context_line = context_line.rstrip(" ; ") + "\n"
                context += context_line
            except Exception as e:
                print(f"Error generating context line: {e}")

        # Control the size of the context
        context += f"\nEstimated number of tokens: {len(context.split())}"
        print(context)
        pyperclip.copy(context)
        print(f"{Fore.GREEN}=================================================> Context copied to clipboard \u2705")

    except Exception as e:
        print(f"Error generating project context: {e}")

    return context


if __name__ == "__main__":
    directory = r"C:/Work/3-GPT-context/Development/src"  # Change to the path of your project directory
    generate_project_context(directory)
