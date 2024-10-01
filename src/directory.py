# directory.py

import os
import json


def init():
    # Lógica para inicializar el contexto
    print("Inicializando el contexto...")

    # Definir la ruta para la carpeta .context y el archivo context.json
    context_dir = os.path.join(os.getcwd(), '.context')
    json_file_path = os.path.join(context_dir, 'context.json')

    # Crear la carpeta .context si no existe
    os.makedirs(context_dir, exist_ok=True)

    # Crear un archivo context.json dentro de la carpeta .context
    context_data = {
        "message": "Configuración inicializada.",
        "version": 1.0
    }

    with open(json_file_path, 'w') as json_file:
        json.dump(context_data, json_file, indent=4)

    print(f"Contexto inicializado. Carpeta creada en: {context_dir}")
    print(f"Archivo JSON creado en: {json_file_path}")
