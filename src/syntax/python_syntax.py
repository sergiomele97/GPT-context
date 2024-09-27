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


# Test de la función
if __name__ == "__main__":
    code_sample = """
class Test:
    def add(self, a, b):
        return a + b

    def print_hello():
        print("Hello World")
        return  # No tiene valor de retorno

class AnotherClass:
    def get_name():
        return "MyName"

    def log(message):
        if a == 1:
            return False
        else:
            return True
        print(message)

# Esta es una función global
def multiply(x, y):
    return x * y

    """

    classes_info, functions_info = extract_functions_and_classes(code_sample)
