from syntax import python_syntax

from syntax import cs_syntax


def get_language(file):
    """Detecta el lenguaje de programación del archivo basado en su extensión."""
    if file.endswith('.py'):
        return 'python'
    elif file.endswith('.js'):
        return 'javascript'
    elif file.endswith('.java'):
        return 'java'
    elif file.endswith('.cs'):
        return 'cs'
    elif file.endswith('.cpp'):
        return 'cpp'
    return None


def extract_info(file, code):
    """Extrae funciones y clases del código basado en el lenguaje."""
    lang = get_language(file)

    if lang == 'python':
        return python_syntax.extract_functions_and_classes(code)
    elif lang == 'javascript':
        return extract_functions_and_classes_javascript(code)
    elif lang == 'java':
        return extract_functions_and_classes_java(code)
    elif lang == 'cs':
        return cs_syntax.extract_functions_and_classes(code)
    elif lang == 'cpp':
        return extract_functions_and_classes_cpp(code)
    return {}, []



def extract_functions_and_classes_javascript(code):
    pass


def extract_functions_and_classes_java(code):
    pass


def extract_functions_and_classes_c(code):
    pass


def extract_functions_and_classes_cpp(code):
    pass