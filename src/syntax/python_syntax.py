import ast


def extract_functions_and_classes(code):
    tree = ast.parse(code)
    classes_info = {}
    functions_info = []

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

    return classes_info, functions_info


def extract_function_info(node, code):
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
    return {
        'name': func_name,
        'params': params,
        'return': return_value
    }
