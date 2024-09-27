import ast


def get_language(file):
    """Detecta el lenguaje de programación del archivo basado en su extensión."""
    if file.endswith('.py'):
        return 'python'
    elif file.endswith('.js'):
        return 'javascript'
    elif file.endswith('.java'):
        return 'java'
    elif file.endswith('.c'):
        return 'c'
    elif file.endswith('.cpp'):
        return 'cpp'
    return None


def extract_info(code, lang):
    """Extrae funciones y clases del código basado en el lenguaje."""
    if lang == 'python':
        return extract_functions_and_classes_python(code)
    elif lang == 'javascript':
        return extract_functions_and_classes_javascript(code)
    elif lang == 'java':
        return extract_functions_and_classes_java(code)
    elif lang == 'c':
        return extract_functions_and_classes_c(code)
    elif lang == 'cpp':
        return extract_functions_and_classes_cpp(code)
    return {}, []


def extract_functions_and_classes_python(code):
    tree = ast.parse(code)
    classes_info = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            class_functions = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    func_name = item.name
                    # Extraer parámetros
                    params = [arg.arg for arg in item.args.args]
                    # Extraer lo que se retorna
                    returns = []
                    for return_node in [n for n in ast.walk(item) if isinstance(n, ast.Return)]:
                        if return_node.value:
                            return_expr = ast.get_source_segment(code, return_node.value)
                            returns.append(return_expr)
                    return_value = ', '.join(returns) if returns else 'None'
                    class_functions.append({
                        'name': func_name,
                        'params': params,
                        'return': return_value
                    })
            classes_info[class_name] = class_functions
    return classes_info

def extract_functions_and_classes_javascript(code):
    pass


def extract_functions_and_classes_java(code):
    pass


def extract_functions_and_classes_c(code):
    pass


def extract_functions_and_classes_cpp(code):
    pass