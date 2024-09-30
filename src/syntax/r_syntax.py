import re

def extract_info(codigo_r):
    # --------------------------------------------------------------------------------------------------- Parámetros

    # ---REGEX---------
    regex_funciones = r'(?<!#)\s*([a-zA-Z_][a-zA-Z0-9_.]*)\s*<-\s*function\s*\(([^)]*)\)'  # Captura funciones
    regex_return = r'return\s*([^#;]*)'  # Captura el valor después del 'return'

    # ---OUTPUT--------
    funciones_globales = []

    # ------------------------------------------------------------------------------------------ Lectura linea a linea
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

    # --- Formatear la salida en el formato requerido
    funciones_info = [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones_globales]

    return funciones_info


# ---------------------------------------------------------------------------------------------------------- TESTING
if __name__ == "__main__":
    # Código R que deseas analizar
    codigo_r = """
    add <- function(a, b) {
        return(a + b)
    }

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
    funciones_info = extract_info(codigo_r)

    # Mostramos los resultados
    print("Funciones encontradas:")
    print(funciones_info)

    # Definir la salida esperada
    salida_esperada_globales = [
        {'name': 'add', 'params': ['a', 'b'], 'return': 'a + b'},
        {'name': 'printHello', 'params': [], 'return': ''},
        {'name': 'multiply', 'params': ['x', 'y'], 'return': 'x * y'}
    ]

    # Comprobamos que los resultados coincidan con la salida esperada
    if funciones_info == salida_esperada_globales:
        print("Prueba exitosa: Los resultados son los esperados.")
    else:
        print("Prueba fallida: Los resultados no coinciden con lo esperado.")
