import os
import argparse

def init_context_repo(repo_path):
    """Inicializa un nuevo repositorio de contexto."""
    context_dir = os.path.join(repo_path, '.context')
    if os.path.exists(context_dir):
        print(f"El repositorio de contexto ya existe en {context_dir}.")
        return

    try:
        # Crear el directorio del repositorio y subdirectorios
        os.makedirs(os.path.join(context_dir, 'history'), exist_ok=True)
        with open(os.path.join(context_dir, 'current_context.txt'), 'w') as f:
            f.write("")

        print(f"Repositorio de contexto inicializado en {context_dir}.")
    except Exception as e:
        print(f"Error al inicializar el repositorio: {e}")

def add_context(repo_path):
    """Agrega la estructura de directorios actual al repositorio de contexto."""
    context_dir = os.path.join(repo_path, '.context')
    context_file = os.path.join(context_dir, 'current_context.txt')
    new_context = generate_compact_directory_structure(os.getcwd())
    
    try:
        if not os.path.exists(context_dir):
            raise FileNotFoundError(f"El directorio de contexto no existe en {context_dir}")
        
        with open(context_file, 'w') as f:
            f.write(new_context)
        
        # Guardar en el historial
        history_path = os.path.join(context_dir, 'history', 'context_history.txt')
        with open(history_path, 'a') as f:
            f.write(new_context + "\n---\n")
        
        print(f"Contexto agregado a {context_file}.")
    except Exception as e:
        print(f"Error al agregar el contexto: {e}")

def generate_compact_directory_structure(root_dir):
    """Genera una representación compacta de la estructura de directorios."""
    def list_compact_dir_structure(directory):
        structure = ""
        try:
            items = sorted(os.listdir(directory))
            if items:
                structure += f"{os.path.basename(directory)}: "
                contents = []
                for item in items:
                    path = os.path.join(directory, item)
                    if os.path.isdir(path):
                        contents.append(f"{list_compact_dir_structure(path)}")
                    else:
                        contents.append(item)
                structure += "(" + ", ".join(contents) + ")"
        except PermissionError:
            structure += "[Acceso Denegado]"
        except Exception as e:
            structure += f"[Error: {e}]"
        return structure
    
    return list_compact_dir_structure(root_dir)

def main():
    parser = argparse.ArgumentParser(description="Herramienta de gestión de contexto.")
    subparsers = parser.add_subparsers(dest='command')

    # Comando 'init'
    init_parser = subparsers.add_parser('init', help='Inicializa un nuevo repositorio de contexto.')
    init_parser.add_argument('path', help='Ruta al directorio del repositorio.')

    # Comando 'add'
    add_parser = subparsers.add_parser('add', help='Agrega el contexto actual al repositorio.')
    add_parser.add_argument('--all', action='store_true', help='Agregar todo el contexto.')

    args = parser.parse_args()

    # La ruta del repositorio se construye correctamente aquí
    repo_path = args.path if args.command == 'init' else os.path.join(os.getcwd(), '.context')

    if args.command == 'init':
        init_context_repo(repo_path)
    elif args.command == 'add':
        if args.all:
            add_context(os.path.dirname(repo_path))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
