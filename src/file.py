import os
import json
from directory import locate_context  # Asegúrate de que esta función esté en directory.py


def add(file_path):
    try:
        # Llamar a locate_context para obtener la ruta de la carpeta .context
        context_dir = locate_context()

        # Ruta del archivo current_context.json
        current_context_file = os.path.join(context_dir, 'current_context.json')

        # Verificar si el archivo current_context.json existe
        if not os.path.exists(current_context_file):
            print(f"No se encontró el archivo: {current_context_file}. Asegúrate de haberlo creado primero.")
            return

        # Cargar el contenido del archivo current_context.json
        with open(current_context_file, 'r') as json_file:
            context_data = json.load(json_file)

        # Verificar si context_data es un diccionario
        if not isinstance(context_data, dict):
            print(f"El archivo JSON no tiene la estructura correcta. Se esperaba un objeto, pero se encontró: {type(context_data)}")
            return

        # Obtener la ruta absoluta del contexto global
        global_context_dir = os.path.join(os.path.expanduser('~'), 'GPT-context', '.context')

        # Determinar si la ruta corresponde al contexto global
        if context_dir == global_context_dir:
            # Guardar ruta absoluta
            file_to_add = os.path.abspath(file_path)
        else:
            # Guardar ruta relativa
            file_to_add = os.path.relpath(file_path, start=os.path.dirname(context_dir))

        # Verificar si el archivo ya está en la lista
        if file_to_add in context_data['files']:
            print(f"El archivo ya está añadido: {file_path}.")
            return

        # Añadir el archivo a la lista
        context_data['files'].append(file_to_add)

        # Guardar los cambios de vuelta en current_context.json
        with open(current_context_file, 'w') as json_file:
            json.dump(context_data, json_file, indent=4)

        print(f"Archivo añadido: {file_path}.")

    except Exception as e:
        print(f"Ocurrió un error al añadir el archivo: {e}")


def check():
    try:
        # Llamar a locate_context para obtener la ruta de la carpeta .context
        context_dir = locate_context()

        # Ruta del archivo current_context.json
        current_context_file = os.path.join(context_dir, 'current_context.json')

        # Verificar si el archivo current_context.json existe
        if not os.path.exists(current_context_file):
            print(f"No se encontró el archivo: {current_context_file}. Asegúrate de haberlo creado primero.")
            return

        # Cargar el contenido del archivo current_context.json
        with open(current_context_file, 'r') as json_file:
            context_data = json.load(json_file)

        # Imprimir el nombre del contexto
        print(f"Contexto actual: {context_data['name']}")

        # Imprimir los archivos listados
        print("Archivos en el contexto:")
        for file_name in context_data.get('files', []):
            print(f"- {file_name}")

            # Intentar abrir e imprimir el contenido del archivo
            try:
                # Construir la ruta del archivo correctamente
                # Suponiendo que el archivo está en el directorio padre de .context
                full_path = os.path.abspath(os.path.join(os.path.dirname(context_dir), file_name))

                with open(full_path, 'r') as file:
                    content = file.read()
                    print(f"Contenido de {file_name}:\n{content}\n")
            except Exception as e:
                print(f"No se pudo leer el archivo {file_name}: {e}")

    except Exception as e:
        print(f"Ocurrió un error al verificar el contexto: {e}")


if __name__ == "__main__":
    # Cambia esta ruta a la ruta del archivo que deseas añadir
    add(r"C:\Work\3-GPT-context\Development\src\language.py")
    check()
