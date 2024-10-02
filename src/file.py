import os
import json
from directory import locate_context  # Asegúrate de que esta función esté en directory.py


# -----------------------------------------------------------
# Función add:
# Añade un archivo al contexto actual.
# -----------------------------------------------------------
def add(file_path):
    try:
        # Obtener contexto actual
        context_dir, current_context_file, context_data = get_current_context()
        if not context_data:
            print(f"No se encontró el archivo {current_context_file} o está vacío.")
            return

        # Obtener la ruta correcta del archivo a añadir
        global_context_dir = os.path.join(os.path.expanduser('~'), 'GPT-context', '.context')
        file_to_add = os.path.abspath(file_path) if context_dir == global_context_dir else os.path.relpath(file_path, start=os.path.dirname(context_dir))

        # Verificar si el archivo ya está en la lista
        if file_to_add in context_data.get('files', []):
            print(f"El archivo ya está añadido: {file_path}.")
            return

        # Añadir el archivo a la lista y guardar los cambios
        context_data.setdefault('files', []).append(file_to_add)
        save_json_file(current_context_file, context_data)

        print(f"Archivo añadido: {file_path}.")

    except Exception as e:
        print(f"Ocurrió un error al añadir el archivo: {e}")


# -----------------------------------------------------------
# Función check:
# Genera el contexto actual (nombre, archivos y contenido).
# -----------------------------------------------------------
def check():
    try:
        # Obtener contexto actual
        context_dir, current_context_file, context_data = get_current_context()
        if not context_data:
            print(f"No se encontró el archivo {current_context_file} o está vacío.")
            return

        # Imprimir el nombre del contexto
        print(f"Contexto actual: {context_data.get('name', 'Sin nombre')}")

        # Imprimir y mostrar el contenido de los archivos listados en el contexto
        print("Archivos en el contexto:")
        for file_name in context_data.get('files', []):
            print(f"- {file_name}")
            try:
                # Ruta correcta del archivo
                full_path = os.path.abspath(os.path.join(os.path.dirname(context_dir), file_name))

                # Leer e imprimir el contenido del archivo
                with open(full_path, 'r') as file:
                    content = file.read()
                    print(f"Contenido de {file_name}:\n{content}\n")
            except Exception as e:
                print(f"No se pudo leer el archivo {file_name}: {e}")

    except Exception as e:
        print(f"Ocurrió un error al verificar el contexto: {e}")


# -----------------------------------------------------------
# Función change_context:
# Cambia el contexto actual al especificado. Antes de cambiar,
# guarda el contexto actual en all_context.json.
# -----------------------------------------------------------
def change_context(new_context_name):
    try:
        # Obtener contexto actual
        context_dir, current_context_file, current_context = get_current_context()
        all_contexts_file = os.path.join(context_dir, 'all_context.json')
        all_contexts = load_json_file(all_contexts_file, default=[])

        # Guardar el contexto actual en all_context.json
        if current_context:
            update_all_contexts(all_contexts, current_context)
            save_json_file(all_contexts_file, all_contexts)

        # Encontrar o crear el nuevo contexto
        new_context = find_or_create_context(all_contexts, new_context_name)

        # Guardar el nuevo contexto en current_context.json
        save_json_file(current_context_file, new_context)

        print(f"Cambiado al contexto '{new_context_name}'.")

    except Exception as e:
        print(f"Ocurrió un error al cambiar el contexto: {e}")


# -----------------------------------------------------------
# Funciones de soporte
# -----------------------------------------------------------

def get_current_context():
    try:
        context_dir = locate_context()
        current_context_file = os.path.join(context_dir, 'current_context.json')
        context_data = load_json_file(current_context_file, default={})
        return context_dir, current_context_file, context_data
    except Exception as e:
        print(f"Ocurrió un error al obtener el contexto actual: {e}")
        return None, None, None


def load_json_file(file_path, default):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as json_file:
                return json.load(json_file)
        except Exception as e:
            print(f"Error al leer {file_path}: {e}")
    return default


def save_json_file(file_path, data):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        print(f"Error al guardar {file_path}: {e}")


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
    # Si no se encuentra, se crea uno nuevo
    print(f"No se encontró el contexto '{new_context_name}'. Creando uno nuevo.")
    new_context = {"name": new_context_name, "files": []}
    all_contexts.append(new_context)
    return new_context

# -----------------------------------------------------------
# Testing
# -----------------------------------------------------------

if __name__ == "__main__":
    add(r"C:\Work\3-GPT-context\Development\src\language.py")
    check()
    change_context("Prueba1")
