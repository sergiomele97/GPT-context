import os
import uuid
from datetime import datetime
import gemini
import context_tools


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

def add_context(prompt):
    # 1. Encuentra el directorio padre
    start_path = os.getcwd()
    context_dir = context_tools.find_context_repo(start_path)

    if not context_dir:
        context_tools.context_not_found(start_path)
        return

    parent_dir = os.path.dirname(context_dir)

    # 2. Genera resumen de directorios
    summary = generate_summary(parent_dir)

    # 3. Genera un JSON con un identificador único, el prompt, el resumen y la datetime actual.

    context_data = {
        'id': str(uuid.uuid4()),  # Genera un ID único con uuid
        'prompt': prompt,
        'summary': summary,
        'timestamp': datetime.now().isoformat()  # Fecha y hora actual en formato ISO
    }

    # 4. Mandar prompt a gemini para que lo resuma
    print(gemini.summarize(context_data))

if __name__ == "__main__":
    add_context("Quiero añadir un nuevo comando a la aplicación")

