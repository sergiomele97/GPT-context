import ast

def extract_imports(code):
    """Extrae las declaraciones de importación del código Python."""
    tree = ast.parse(code)
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)  # Añadir el módulo
            for alias in node.names:
                imports.append(f"{node.module}.{alias.name}")  # Añadir la función o clase

    return imports

def extract_info(code):
    """Extrae imports, funciones y clases del código Python."""
    tree = ast.parse(code)
    classes_info = {}
    functions_info = []

    # Extraer imports
    imports = extract_imports(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            class_functions = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    func_info = extract_function_info(item, code)
                    class_functions.append(func_info)
            classes_info[class_name] = class_functions
        elif isinstance(node, ast.FunctionDef):
            func_info = extract_function_info(node, code)
            functions_info.append(func_info)

    return imports, classes_info, functions_info  # Cambiar el retorno

def extract_function_info(node, code):
    """Extrae información sobre funciones individuales."""
    func_name = node.name
    params = [arg.arg for arg in node.args.args]
    returns = []
    for return_node in [n for n in ast.walk(node) if isinstance(n, ast.Return)]:
        if return_node.value:
            return_expr = ast.get_source_segment(code, return_node.value)
            returns.append(return_expr)
    return_value = ', '.join(returns) if returns else 'None'
    return {
        'name': func_name,
        'params': params,
        'return': return_value
    }

def generate_summary(code_files):
    """Genera un resumen de los archivos de código, incluyendo imports, clases y funciones."""
    summary = []
    for file_path, code in code_files:
        try:
            # Extraer imports, clases y funciones del código
            imports, classes, functions = extract_info(code)
        except Exception as e:
            print(f"Error procesando {file_path}: {e}")
            continue
        # Agregar resultados al resumen
        summary.append((file_path, imports, classes, functions))

    return summary

# Test de la función
if __name__ == "__main__":
    code_sample = """
import os
from datetime import datetime

class Test:
    def add(self, a, b):
        return a + b

    def print_hello(self):
        print("Hello World")
        return  # No tiene valor de retorno

class AnotherClass:
    def get_name(self):
        return "MyName"

    def log(self, message):
        if message == "Hello":
            return False
        else:
            return True

def multiply(x, y):
    return x * y
"""

    code_files = [("test_file.py", code_sample)]
    summary = generate_summary(code_files)
    print(summary)
