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
from syntax import r_syntax
from syntax import kotlin_syntax
from syntax import perl_syntax
from syntax import rust_syntax
from syntax import c_syntax

def extract_info(file, code):
    """Detecta el lenguaje de programación basado en la extensión del archivo y extrae funciones y clases del código."""

    # Diccionario para mapear extensiones a funciones de extracción
    syntax_extractors = {
        '.py': python_syntax.extract_info,
        '.js': javascript_syntax.extract_info,
        '.java': java_syntax.extract_info,
        '.php': php_syntax.extract_info,
        '.cs': cs_syntax.extract_info,
        '.cpp': cpp_syntax.extract_info,
        '.c++': cpp_syntax.extract_info,
        '.c': c_syntax.extract_info,
        '.rb': ruby_syntax.extract_info,
        '.swift': swift_syntax.extract_info,
        '.ts': typescript_syntax.extract_info,
        '.go': go_syntax.extract_info,
        '.r': r_syntax.extract_info,
        '.kt': kotlin_syntax.extract_info,
        '.pl': perl_syntax.extract_info,
        '.rs': rust_syntax.extract_info,
    }

    # Determinar el lenguaje basado en la extensión del archivo
    for extension, extractor in syntax_extractors.items():
        if file.endswith(extension):
            try:
                return extractor(code)
            except Exception as e:
                print(f"Error extracting info for {file}: {e}")
                return {}, []  # Retornar valores por defecto en caso de error

    # Si el archivo no coincide con ningún lenguaje soportado
    print(f"Unsupported file type: {file}")
    return {}, []  # Retornar valores por defecto si el tipo de archivo no es soportado
