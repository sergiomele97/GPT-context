import os
import re
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

        # Obtener el nombre del contexto
        context_name = context_data.get('name', None)
        if not context_name:
            print("El contexto actual no tiene un nombre definido.")
            return

        print(f"Contexto actual: {context_name}")

        # Imprimir y mostrar el contenido de los archivos listados en el contexto
        print("Archivos en el contexto:")
        for file_name in context_data.get('files', []):
            print(f"- {file_name}")
            try:
                # Ruta correcta del archivo
                full_path = os.path.abspath(os.path.join(os.path.dirname(context_dir), file_name))

                # Leer el contenido del archivo
                with open(full_path, 'r') as file:
                    content = file.read()

                    # Llamar al método para extraer los fragmentos delimitados
                    fragments = extract_fragments(content, context_name)

                    # Si no se encuentran fragmentos, mostrar el archivo completo
                    if not fragments:
                        print(
                            f"No se encontraron fragmentos específicos para el contexto '{context_name}' en {file_name}. Mostrando el archivo completo:\n{content}\n")
                    else:
                        # Mostrar cada fragmento extraído
                        for fragment in fragments:
                            print(f"Fragmento de {file_name} para el contexto '{context_name}':\n{fragment}\n")

            except Exception as e:
                print(f"No se pudo leer el archivo {file_name}: {e}")

    except Exception as e:
        print(f"Ocurrió un error al verificar el contexto: {e}")


def extract_fragments(content, context_name):
    """
    Extrae todos los fragmentos delimitados por CONTEXT_<context_name>_START y CONTEXT_<context_name>_END.

    Args:
    - content: El contenido del archivo.
    - context_name: El nombre del contexto que se usa para encontrar las etiquetas.

    Returns:
    - Una lista de fragmentos extraídos entre las etiquetas de inicio y fin.
    """
    # Etiquetas de inicio y fin
    start_tag = f"CONTEXT_{context_name}_START"
    end_tag = f"CONTEXT_{context_name}_END"

    # Encontrar todas las posiciones de inicio y fin de los fragmentos
    start_positions = [match.end() for match in re.finditer(start_tag, content)]
    end_positions = [match.start() for match in re.finditer(end_tag, content)]

    # Si no hay posiciones de inicio, devolver una lista vacía
    if not start_positions:
        return []

    # Asegurarnos de que haya suficientes etiquetas de fin, si no, extendemos hasta el final
    if len(end_positions) < len(start_positions):
        end_positions.append(len(content))  # Añadir el final del archivo como último posible fin

    # Extraer los fragmentos entre cada par de etiquetas
    fragments = []
    for start_idx, end_idx in zip(start_positions, end_positions):
        fragment = content[start_idx:end_idx].strip()
        fragments.append(fragment)

    return fragments


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

def list():
    try:
        context_dir = locate_context()
        all_context_dir = os.path.join(context_dir, 'all_context.json')
        all_context_data = load_json_file(all_context_dir, default=[])

        # Imprimir el listado de contextos de forma personalizada
        print("Listado de contextos:")
        for context in all_context_data:
            name = context.get('name', 'sin nombre')
            files = context.get('files', [])
            files_list = ', '.join(files) if files else 'sin archivos'
            print(f' - Contexto: "{name}", Contenido: Archivos: {files_list}')
    except Exception as e:
        print(f"Ocurrió un error al listar los contextos: {e}")
    


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
    #check()
    list()
