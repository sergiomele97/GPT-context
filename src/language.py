from syntax import python_syntax
from syntax import cs_syntax
from syntax import javascript_syntax
from syntax import java_syntax
from syntax import cpp_syntax
from syntax import php_syntax
from syntax import ruby_syntax
from syntax import swift_syntax
from syntax import typescript_syntax
from syntax import go_syntax
from syntax import shell_syntax
from syntax import css_syntax
from syntax import scala_syntax
from syntax import r_syntax
from syntax import objc_syntax  # Objective-C
from syntax import powershell_syntax
from syntax import kotlin_syntax
from syntax import perl_syntax
from syntax import rust_syntax
from syntax import c_syntax


def extract_info(file, code):
    """Detecta el lenguaje de programación basado en la extensión del archivo y extrae funciones y clases del código."""

    if file.endswith('.py'):
        return python_syntax.extract_functions_and_classes(code)
    elif file.endswith('.js'):
        return javascript_syntax.extract_functions_and_classes(code)
    elif file.endswith('.java'):
        return java_syntax.extract_functions_and_classes(code)
    elif file.endswith('.php'):
        return php_syntax.extract_functions_and_classes(code)
    elif file.endswith('.cs'):
        return cs_syntax.extract_functions_and_classes(code)
    elif file.endswith('.cpp') or file.endswith('.c++'):
        return cpp_syntax.extract_functions_and_classes(code)
    elif file.endswith('.c'):
        return c_syntax.extract_functions_and_classes(code)
    elif file.endswith('.rb'):
        return ruby_syntax.extract_functions_and_classes(code)
    elif file.endswith('.swift'):
        return swift_syntax.extract_functions_and_classes(code)
    elif file.endswith('.ts'):
        return typescript_syntax.extract_functions_and_classes(code)
    elif file.endswith('.go'):
        return go_syntax.extract_functions_and_classes(code)
    elif file.endswith('.sh'):
        return shell_syntax.extract_commands(code)  # Para shell scripts
    elif file.endswith('.ps1'):
        return powershell_syntax.extract_functions_and_classes(code)  # Para PowerShell
    elif file.endswith('.css'):
        return css_syntax.extract_selectors(code)  # Para CSS
    elif file.endswith('.r'):
        return r_syntax.extract_functions_and_classes(code)  # Para R
    elif file.endswith('.m'):
        return objc_syntax.extract_functions_and_classes(code)  # Para Objective-C
    elif file.endswith('.scala'):
        return scala_syntax.extract_functions_and_classes(code)  # Para Scala
    elif file.endswith('.kt'):
        return kotlin_syntax.extract_functions_and_classes(code)  # Para Kotlin
    elif file.endswith('.pl'):
        return perl_syntax.extract_functions_and_classes(code)  # Para Perl
    elif file.endswith('.rs'):
        return rust_syntax.extract_functions_and_classes(code)  # Para Rust

    # Si el archivo no coincide con ningún lenguaje soportado
    return {}, []
