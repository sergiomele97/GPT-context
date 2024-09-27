import os

from src.syntax import python_syntax


def read_code_files(directory):
    code_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.js', '.java')):  # Cambia según tus necesidades
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    code_files.append((file_path, f.read()))
    return code_files


def generate_summary(code_files):
    summary = []
    for file_path, code in code_files:
        classes, functions = python_syntax.extract_functions_and_classes(code)
        summary.append((file_path, classes, functions))
    return summary


def generate_project_context(directory, project_description):
    print(f"Generando contexto para el proyecto en: {directory}")
    code_files = read_code_files(directory)
    summary = generate_summary(code_files)

    context = f"### Contexto del Proyecto\n"
    context += f"**Descripción del Proyecto:** {project_description}\n\n"

    # Optimización de la estructura de archivos
    context += f"**Te paso la estructura de archivos del proyecto con sus funciones (parámetros) -> salidas:**\n"

    for file_path, classes, functions in summary:
        context_line = f"{file_path}: "

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

    return context


if __name__ == "__main__":
    directory = r"C:\Work\3-GPT-context\src"  # Cambia a la ruta del directorio de tu proyecto
    project_description = "Este proyecto es una aplicación para resumir y analizar código."  # Cambia esta descripción según tu proyecto
    project_context = generate_project_context(directory, project_description)

    # Controlar el tamaño del contexto
    print("### Contexto Generado ###")
    print(project_context)
    print(f"\nNúmero de tokens estimados: {len(project_context.split())}")  # Aproximación de tokens
