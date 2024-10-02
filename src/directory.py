import os
import json


# -----------------------------------------------------------
# Función init:
# Inicializa el contexto creando una carpeta .context y un
# archivo context.json con información sobre contextos
# personalizados. Si la carpeta ya existe, se informará al
# usuario y no se realizarán cambios adicionales.
# -----------------------------------------------------------
def init():
    try:
        # Lógica para inicializar el contexto
        print("Inicializando el contexto...")

        # Definir la ruta para la carpeta .context y el archivo context.json
        context_dir = os.path.join(os.getcwd(), '.context')
        json_file_path = os.path.join(context_dir, 'context.json')

        # Verificar si la carpeta .context ya existe
        if os.path.exists(context_dir):
            print(f"La carpeta '.context' ya existe en: {context_dir}")
        else:
            # Crear la carpeta .context si no existe
            os.makedirs(context_dir)
            create_json(json_file_path)

            print(f"Contexto inicializado. Carpeta creada en: {context_dir}")
            print(f"Archivo JSON creado en: {json_file_path}")

    except Exception as e:
        print(f"Ocurrió un error al inicializar el contexto: {e}")


# -----------------------------------------------------------
# Función locate_context:
# Busca la carpeta .context en el directorio actual y sus
# padres. Si no la encuentra, busca en la carpeta global
# C:\Program Files\GPT-context. Crea la carpeta global si
# no existe y devuelve la ruta correspondiente.
# -----------------------------------------------------------
def locate_context():
    # Definir la ruta global donde debe estar el contexto predeterminado
    global_context_dir = os.path.join(os.path.expanduser('~'), 'GPT-context', '.context')

    # Comenzar desde el directorio actual
    current_dir = os.getcwd()

    while True:
        # Definir la ruta para la carpeta .context en el directorio actual
        context_dir = os.path.join(current_dir, '.context')

        try:
            # Verificar si la carpeta .context existe en el directorio actual
            if os.path.exists(context_dir):
                print(f"Contexto local encontrado en: {context_dir}")
                return context_dir
        except Exception as e:
            print(f"Ocurrió un error al verificar el contexto local: {e}")
            return None  # Retornar None para indicar un fallo

        # Subir un nivel en el directorio padre
        parent_dir = os.path.dirname(current_dir)

        # Si hemos llegado al directorio raíz, salir del bucle
        if parent_dir == current_dir:
            break

        current_dir = parent_dir

    # Si no se encontró contexto local, verificar el contexto global
    try:
        if not os.path.exists(global_context_dir):
            os.makedirs(global_context_dir)
            print(f"Contexto global creado en: {global_context_dir}")

            json_file_path = os.path.join(global_context_dir, 'context.json')
            create_json(json_file_path)
            print(f"Archivo JSON creado en: {json_file_path}")

    except Exception as e:
        print(f"Ocurrió un error al crear el contexto global: {e}")

    print(f"Usando contexto global en: {global_context_dir}")
    return global_context_dir


# -----------------------------------------------------------
# Función create_json:
# Crear un archivo context.json estandar dentro de la carpeta .context
# -----------------------------------------------------------
def create_json(json_file_path):

    context_data = [
        {
            "name": "context_ejemplo1",
            "files": ["file1.py", "file2.js"]
        },
        {
            "name": "context_ejemplo2",
            "files": ["file3.java", "file4.cpp"]
        }
    ]
    # Guardar los contextos en el archivo JSON
    with open(json_file_path, 'w') as json_file:
        json.dump(context_data, json_file, indent=4)

# -----------------------------------------------------------
# Testing
# -----------------------------------------------------------
if __name__ == "__main__":
    init()
    locate_context()
