import os
import ast


def read_code_files(directory):
    code_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.js', '.java')):  # Cambia según tus necesidades
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    code_files.append((file_path, f.read()))
    return code_files


def extract_functions_and_classes(code):
    tree = ast.parse(code)
    functions_info = []
    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            # Extraer parámetros
            params = [arg.arg for arg in node.args.args]
            # Extraer lo que se retorna
            returns = []
            for return_node in [n for n in ast.walk(node) if isinstance(n, ast.Return)]:
                if return_node.value:
                    return_expr = ast.get_source_segment(code, return_node.value)
                    returns.append(return_expr)
            return_value = ', '.join(returns) if returns else 'None'
            functions_info.append({
                'name': func_name,
                'params': params,
                'return': return_value
            })

    return functions_info, classes


def prioritize_functions(functions):
    return functions[:10]  # Retornar las primeras 10 funciones por ahora.


def prioritize_classes(classes):
    return classes[:10]  # Retornar las primeras 10 clases por ahora.


def generate_summary(code_files):
    summary = {'functions': [], 'classes': [], 'file_count': len(code_files)}
    for file_path, code in code_files:
        functions, classes = extract_functions_and_classes(code)
        summary['functions'].extend(functions)
        summary['classes'].extend(classes)

    # Priorizar funciones y clases
    summary['functions'] = prioritize_functions(summary['functions'])
    summary['classes'] = prioritize_classes(summary['classes'])

    return summary


def generate_project_context(directory, project_description):
    print(f"Generando contexto para el proyecto en: {directory}")
    code_files = read_code_files(directory)
    summary = generate_summary(code_files)

    context = f"### Contexto del Proyecto\n"
    context += f"**Descripción del Proyecto:** {project_description}\n\n"

    # Optimización de la estructura de archivos
    context += f"**Estructura de Archivos:**\n"

    file_info = {}
    for file_path, code in code_files:
        # Extraer funciones con parámetros y retornos
        functions, _ = extract_functions_and_classes(code)
        file_info[file_path] = functions

    for file_path, functions in file_info.items():
        context += f"- {file_path}:\n"
        for func in functions:
            params = ', '.join(func['params']) if func['params'] else 'sin parámetros'
            context += f"  - Función: {func['name']}({params}) -> {func['return']}\n"

    context += f"\n**Funciones Principales:** {', '.join([func['name'] for func in summary['functions']])}\n"
    context += f"**Clases Principales:** {', '.join(summary['classes'])}\n"

    return context


if __name__ == "__main__":
    directory = r"C:\Work\3-GPT-context\src"  # Cambia a la ruta del directorio de tu proyecto
    project_description = "Este proyecto es una aplicación para resumir y analizar código."  # Cambia esta descripción según tu proyecto
    project_context = generate_project_context(directory, project_description)

    # Controlar el tamaño del contexto
    print("### Contexto Generado ###")
    print(project_context)
    print(f"\nNúmero de tokens estimados: {len(project_context.split())}")  # Aproximación de tokens
