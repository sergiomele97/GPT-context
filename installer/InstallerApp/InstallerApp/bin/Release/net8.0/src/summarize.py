import os
import language


def read_code_files(directory):
    code_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.js', '.java', '.php', '.cs', '.cpp', '.c++', '.c',
                              '.rb', '.swift', '.ts', '.go', '.r', '.kt', '.pl', '.rs')):  # Cambia según tus necesidades
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    code_files.append((file_path, f.read()))
    return code_files


def generate_summary(code_files):
    summary = []
    current_dir = os.getcwd()

    for file_path, code in code_files:
        try:
            # Convierte la ruta absoluta a una ruta relativa basada en el directorio actual
            relative_path = os.path.relpath(file_path, current_dir)

            # Intenta extraer los imports, clases y funciones del archivo
            imports, classes, functions = language.extract_info(file_path, code)
        except Exception as e:
            # Maneja la excepción, registrando el error pero permitiendo que el proceso continúe
            print(f"Error procesando {file_path}: {e}")
            continue  # Pasa al siguiente archivo en lugar de detener la ejecución
        # Si todo está bien, añade los resultados al resumen
        summary.append((relative_path, imports, classes, functions))

    return summary


def generate_project_context(directory):
    print(f"Generando contexto para el proyecto a partir del directorio {directory}\n")
    print(f"(Si esto tarda demasiado puede que se este analizando alguna carpeta de modulos o entorno virtual por error, trata de excluir directorios pesados)\n\n")
    code_files = read_code_files(directory)
    summary = generate_summary(code_files)

    context = f"### Contexto del Proyecto situado en:{os.getcwd()}\n"
    context += f"**Te paso la estructura de archivos del proyecto con su ruta relativa, imports, clases y funciones (parámetros) -> salidas:**\n\n"

    for file_path, imports, classes, functions in summary:
        context_line = f"{file_path}: "

        # Agregar imports
        if imports:
            context_line += f"Imports: {', '.join(imports)}; "

        # Agregar clases y funciones
        for class_name, class_functions in classes.items():
            context_line += f"Class {class_name}: "
            func_lines = []
            for func in class_functions:
                params = ', '.join(func['params']) if func['params'] else 'sin parámetros'
                func_lines.append(f"{func['name']}({params}) -> {func['return']}")
            functions_line = '; '.join(func_lines)
            context_line += f"{functions_line} ; "

        # Agregar funciones que no pertenecen a ninguna clase
        if functions:
            func_lines = []
            for func in functions:
                params = ', '.join(func['params']) if func['params'] else 'sin parámetros'
                func_lines.append(f"{func['name']}({params}) -> {func['return']}")
            functions_line = '; '.join(func_lines)
            context_line += f"No class: {functions_line} ; "

        # Remover el último "; " y agregar nueva línea
        context_line = context_line.rstrip(" ; ") + "\n"
        context += context_line

    # Controlar el tamaño del contexto
    context += f"\nNúmero de tokens estimados: {len(context.split())}"

    return context


if __name__ == "__main__":
    directory = r"C:\Work\3-GPT-context\src"  # Cambia a la ruta del directorio de tu proyecto

    project_context = generate_project_context(directory)
    print(project_context)


