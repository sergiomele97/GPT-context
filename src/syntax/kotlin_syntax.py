import re

def extract_info(codigo_kotlin):
    # --------------------------------------------------------------------------------------------------- Parámetros

    # ---REGEX---------
    regex_clases = r'class\s+([A-Za-z_][A-Za-z0-9_]*)'
    regex_funciones = r'fun\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*(:\s*[A-Za-z_][A-Za-z0-9_]*)?\s*{'
    regex_return = r'return\s+([^;]+);?'  # Capturar el valor después del 'return'

    # ---OUTPUT--------
    clases_y_funciones = {}
    funciones_globales = []

    # ---VARIABLES-----
    clase_actual = None
    llaves_abiertas = 0  # Contador de {}
    funcion_con_parametros = None  # Inicializar aquí para evitar el error

    # ------------------------------------------------------------------------------------------ Lectura línea a línea
    lineas = codigo_kotlin.splitlines()

    for linea in lineas:
        llaves_abiertas += linea.count('{') - linea.count('}')

        # ----------------------------------- Buscar clases
        clase = re.search(regex_clases, linea)
        if clase:
            clase_actual = clase.group(1)
            clases_y_funciones[clase_actual] = []  # Inicializar la lista de funciones para esta clase
            llaves_abiertas = 1
            continue

        # ------------------------------------ Buscar funciones
        funcion = re.search(regex_funciones, linea)
        if funcion:
            nombre_funcion = funcion.group(1)
            parametros = funcion.group(2).split(',') if funcion.group(2).strip() else []
            parametros = [param.strip() for param in parametros]  # Limpiar espacios
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': ''}

            if clase_actual and llaves_abiertas > 0:
                # Si estamos dentro de una clase, agregamos la función a esa clase
                clases_y_funciones[clase_actual].append(funcion_con_parametros)
            else:
                # Si no estamos dentro de una clase, es una función global
                funciones_globales.append(funcion_con_parametros)

        # ------------------------------------ Buscar return usando regex
        retorno = re.search(regex_return, linea)
        if retorno and funcion_con_parametros:  # Verificar que funcion_con_parametros está inicializada
            valor_retorno = retorno.group(1).strip()
            if funcion_con_parametros['return']:
                funcion_con_parametros['return'] += f"; {valor_retorno}"  # Añadir con separación
            else:
                funcion_con_parametros['return'] = valor_retorno  # Almacenar solo el valor de retorno

        # Si las llaves llegan a 0, salimos de la clase
        if llaves_abiertas == 0:
            clase_actual = None

    # --- Formatear la salida en el formato requerido
    clases_info = {clase: [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones]
                   for clase, funciones in clases_y_funciones.items()}
    funciones_info = [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones_globales]

    return clases_info, funciones_info


# ---------------------------------------------------------------------------------------------------------- TESTING
if __name__ == "__main__":
    # Código Kotlin de ejemplo
    codigo_kotlin = """
    class Test {
        fun add(a: Int, b: Int): Int {
            return a + b
        }

        fun printHello() {
            println("Hello World")
            return  
        }
    }

    class AnotherClass {
        fun getName(): String {
            return "MyName"
        }

        private fun log(message: String) {
            if (a == 1) { return false }
            else { return true }
            println(message)
        }
    }

    // Esta es una función global
    fun multiply(x: Int, y: Int): Int {
        return x * y
    }
    """  # Código Kotlin que deseas analizar

    # Llamamos a la función y obtenemos los resultados
    clases_info, funciones_info = extract_info(codigo_kotlin)

    # Mostramos los resultados
    print("Clases y funciones encontradas:")
    print(clases_info)
    print("Funciones globales encontradas:")
    print(funciones_info)

    # Definir la salida esperada
    salida_esperada_clases = {
        'Test': [
            {'name': 'add', 'params': ['a: Int', 'b: Int'], 'return': 'a + b'},
            {'name': 'printHello', 'params': [], 'return': ''}  # Cambiado para reflejar que no hay retorno
        ],
        'AnotherClass': [
            {'name': 'getName', 'params': [], 'return': '"MyName"'},
            {'name': 'log', 'params': ['message: String'], 'return': 'false; true'}
        ]
    }

    salida_esperada_globales = [
        {'name': 'multiply', 'params': ['x: Int', 'y: Int'], 'return': 'x * y'}
    ]

    # Comprobamos que los resultados coincidan con la salida esperada
    if clases_info == salida_esperada_clases and funciones_info == salida_esperada_globales:
        print("Prueba exitosa: Los resultados son los esperados.")
    else:
        print("Prueba fallida: Los resultados no coinciden con lo esperado.")
