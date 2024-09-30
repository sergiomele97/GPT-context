import re


def extract_info(codigo_r):
    # --------------------------------------------------------------------------------------------------- Parámetros

    # ---REGEX---------
    regex_funciones = r'(?<!#)\s*([a-zA-Z_][a-zA-Z0-9_.]*)\s*<-\s*function\s*\(([^)]*)\)'  # Captura funciones
    regex_return = r'return\s*([^#;]*)'  # Captura el valor después del 'return'
    regex_imports = r'(?<!#)\s*library\s*\(([^)]+)\)'  # Captura imports de librerías
    regex_imports_alt = r'(?<!#)\s*require\s*\(([^)]+)\)'  # Captura imports alternativos

    # ---OUTPUT--------
    funciones_globales = []
    imports_globales = []

    # ------------------------------------------------------------------------------------------ Lectura línea a línea
    lineas = codigo_r.splitlines()

    for linea in lineas:
        # ------------------------------------ Buscar funciones
        funcion = re.search(regex_funciones, linea)
        if funcion:
            nombre_funcion = funcion.group(1)
            parametros = funcion.group(2).split(',') if funcion.group(2).strip() else []
            parametros = [param.strip() for param in parametros]  # Limpiar espacios
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': ''}

            funciones_globales.append(funcion_con_parametros)

        # ------------------------------------ Buscar return usando regex
        retorno = re.search(regex_return, linea)
        if retorno and funciones_globales:  # Verificar que funciones_globales no esté vacía
            valor_retorno = retorno.group(1).strip()
            if valor_retorno == '':  # Si no hay valor, no asignar nada
                funciones_globales[-1]['return'] = ''
            else:
                funciones_globales[-1]['return'] = valor_retorno  # Almacenar el valor de retorno de la última función

        # ------------------------------------ Buscar imports usando regex
        import_match = re.search(regex_imports, linea) or re.search(regex_imports_alt, linea)
        if import_match:
            libreria = import_match.group(1).strip()
            imports_globales.append(libreria)  # Almacenar el nombre de la librería

    # --- Formatear la salida en el formato requerido
    funciones_info = [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones_globales]
    clases_info = []
    return imports_globales,clases_info, funciones_info


# ---------------------------------------------------------------------------------------------------------- TESTING
if __name__ == "__main__":
    # Código R que deseas analizar
    codigo_r = """
    library(ggplot2)
    add <- function(a, b) {
        return(a + b)
    }

    require(dplyr)

    printHello <- function() {
        print("Hello World")
        return()  # No tiene valor de retorno
    }

    # Esta es una función global
    multiply <- function(x, y) {
        return(x * y)
    }
    """

    # Llamamos a la función y obtenemos los resultados
    imports_info, funciones_info = extract_info(codigo_r)

    # Mostramos los resultados
    print("Imports encontrados:")
    print(imports_info)
    print("Funciones encontradas:")
    print(funciones_info)

    # Definir la salida esperada
    salida_esperada_imports = ['ggplot2', 'dplyr']
    salida_esperada_globales = [
        {'name': 'add', 'params': ['a', 'b'], 'return': 'a + b'},
        {'name': 'printHello', 'params': [], 'return': ''},
        {'name': 'multiply', 'params': ['x', 'y'], 'return': 'x * y'}
    ]

    # Comprobamos que los resultados coincidan con la salida esperada
    if imports_info == salida_esperada_imports:
        print("Prueba de imports exitosa: Los resultados son los esperados.")
    else:
        print("Prueba de imports fallida: Los resultados no coinciden con lo esperado.")

    if funciones_info == salida_esperada_globales:
        print("Prueba de funciones exitosa: Los resultados son los esperados.")
    else:
        print("Prueba de funciones fallida: Los resultados no coinciden con lo esperado.")
