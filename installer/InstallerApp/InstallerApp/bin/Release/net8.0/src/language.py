from syntax import python_syntax
from syntax import cs_syntax
from syntax import javascript_syntax
from syntax import java_syntax
from syntax import cpp_syntax
from syntax import php_syntax
from syntax import ruby_syntax  #revisar
from syntax import swift_syntax
from syntax import typescript_syntax
from syntax import go_syntax
from syntax import r_syntax
from syntax import kotlin_syntax
from syntax import perl_syntax
from syntax import rust_syntax
from syntax import c_syntax


def extract_info(file, code):
    """Detecta el lenguaje de programación basado en la extensión del archivo y extrae funciones y clases del código."""

    if file.endswith('.py'):
        return python_syntax.extract_info(code)
    elif file.endswith('.js'):
        return javascript_syntax.extract_info(code)
    elif file.endswith('.java'):
        return java_syntax.extract_info(code)
    elif file.endswith('.php'):
        return php_syntax.extract_info(code)
    elif file.endswith('.cs'):
        return cs_syntax.extract_info(code)
    elif file.endswith('.cpp') or file.endswith('.c++'):
        return cpp_syntax.extract_info(code)
    elif file.endswith('.c'):
        return c_syntax.extract_info(code)
    elif file.endswith('.rb'):
        return ruby_syntax.extract_info(code)
    elif file.endswith('.swift'):
        return swift_syntax.extract_info(code)
    elif file.endswith('.ts'):
        return typescript_syntax.extract_info(code)
    elif file.endswith('.go'):
        return go_syntax.extract_info(code)
    elif file.endswith('.r'):
        return r_syntax.extract_info(code)  # Para R
    elif file.endswith('.kt'):
        return kotlin_syntax.extract_info(code)  # Para Kotlin
    elif file.endswith('.pl'):
        return perl_syntax.extract_info(code)  # Para Perl
    elif file.endswith('.rs'):
        return rust_syntax.extract_info(code)  # Para Rust

    # Si el archivo no coincide con ningún lenguaje soportado
    return {}, []

    #CONTEXT_Prueba1_START
    # QUE PASAAAAAAAAAAAAAAAAAAAAAAAAAA CONTEXT_Prueba1_END

    # CONTEXT_Prueba1_START
    # QUE PASAAAAAAAAAAAAAAAAAAAAAAAAAA CONTEXT_Prueba1_END

# CONTEXT_Prueba1_START
# QUE PASAAAAAAAAAAAAAFGDFGAAAAAAAAAAAAA CONTEXT_Prueba1_END
