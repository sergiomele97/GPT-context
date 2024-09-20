import os
import sys


def generate_summary(start_path):
    """Genera un resumen compacto de la estructura de directorios desde start_path."""
    summary = []

    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 2 * level  # Ajusta la indentación según sea necesario

        if files or dirs:  # Solo añade directorios con archivos o subdirectorios
            formatted_root = f"{indent}{os.path.basename(root)}/"
            sub_items = []

            # Formatea archivos
            if files:
                file_list = ','.join(files)
                sub_items.append(f"({file_list})")

            # Formatea subdirectorios
            if dirs:
                sub_items.extend(f"{d}/" for d in dirs)

            if sub_items:
                summary.append(f"{formatted_root}{', '.join(sub_items)}")

    summary_text = '\n'.join(summary)

    return summary_text

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