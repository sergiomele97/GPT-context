import os
import uuid
from datetime import datetime
import gemini
import directory

class prueba:
    numero = 1
    def add(a,b):
        return a + b

def add_context(prompt):


    # 1. Encuentra el directorio padre
    start_path = os.getcwd()
    context_dir = directory.find_context_repo(start_path)

    if not context_dir:
        directory.context_not_found(start_path)
        return

    parent_dir = os.path.dirname(context_dir)

    # 2. Genera resumen de directorios
    summary = directory.generate_summary(parent_dir)

    # 3. Le pedimos a gemini que elija los archivos más importantes
    file_list = gemini.choose_files(summary)
    print(file_list)

    print(gemini.summarize_files(file_list))

    # X. Genera un JSON con un identificador único, el prompt, el resumen y la datetime actual.
    '''
    context_data = {
        'id': str(uuid.uuid4()),  # Genera un ID único con uuid
        'prompt': prompt,
        'summary': summary,
        'timestamp': datetime.now().isoformat()  # Fecha y hora actual en formato ISO
    }
    '''

if __name__ == "__main__":
    add_context("Quiero añadir un nuevo comando a la aplicación")

