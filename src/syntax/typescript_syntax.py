import re

def extract_info(codigo_typescript):
    # --------------------------------------------------------------------------------------------------- Parámetros

    # ---REGEX---------
    regex_clases = r'class\s+([A-Za-z_][A-Za-z0-9_]*)'
    regex_funciones_clase = r'([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*:\s*([A-Za-z_][A-Za-z0-9_]*)?\s*\{'
    regex_funciones_globales = r'function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*:\s*([A-Za-z_][A-Za-z0-9_]*)?\s*\{'
    regex_arrow_functions = r'const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\(([^)]*)\)\s*:\s*([A-Za-z_][A-Za-z0-9_]*)?\s*=>\s*\{'
    regex_return = r'return\s+([^;]+);?'  # Capturar el valor después del 'return'
    # Ignorar bloques como if, for, while
    regex_control_blocks = r'\b(if|else|for|while|switch|catch|try|finally)\b'

    # ---OUTPUT--------
    clases_y_funciones = {}
    funciones_globales = []

    # ---VARIABLES-----
    clase_actual = None
    llaves_abiertas = 0  # Contador de {}
    funcion_con_parametros = None  # Inicializar aquí para evitar el error

    # ------------------------------------------------------------------------------------------ Lectura línea a línea
    lineas = codigo_typescript.splitlines()

    for linea in lineas:
        # Actualizar el contador de llaves abiertas
        llaves_abiertas += linea.count('{') - linea.count('}')

        # Ignorar bloques de control como if, else, for, etc.
        if re.search(regex_control_blocks, linea):
            continue

        # ----------------------------------- Buscar clases
        clase = re.search(regex_clases, linea)
        if clase:
            clase_actual = clase.group(1)
            clases_y_funciones[clase_actual] = []  # Inicializar la lista de funciones para esta clase
            llaves_abiertas = 1
            continue

        # ------------------------------------ Buscar funciones dentro de clases
        funcion_clase = re.search(regex_funciones_clase, linea)
        if funcion_clase:
            nombre_funcion = funcion_clase.group(1)
            parametros = funcion_clase.group(2).split(',') if funcion_clase.group(2).strip() else []
            return_type = funcion_clase.group(3) if funcion_clase.group(3) else "None"
            parametros = [param.strip().split(':')[0] for param in parametros]  # Limpiar espacios y extraer solo el nombre del parámetro
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': return_type}

            if clase_actual:
                clases_y_funciones[clase_actual].append(funcion_con_parametros)
            continue

        # ------------------------------------ Buscar funciones globales (con 'function')
        funcion_global = re.search(regex_funciones_globales, linea)
        if funcion_global:
            nombre_funcion = funcion_global.group(1)
            parametros = funcion_global.group(2).split(',') if funcion_global.group(2).strip() else []
            return_type = funcion_global.group(3) if funcion_global.group(3) else "None"
            parametros = [param.strip().split(':')[0] for param in parametros]  # Limpiar espacios y extraer solo el nombre del parámetro
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': return_type}

            funciones_globales.append(funcion_con_parametros)
            continue

        # ------------------------------------ Buscar funciones flecha (arrow functions)
        funcion_flecha = re.search(regex_arrow_functions, linea)
        if funcion_flecha:
            nombre_funcion = funcion_flecha.group(1)
            parametros = funcion_flecha.group(2).split(',') if funcion_flecha.group(2).strip() else []
            return_type = funcion_flecha.group(3) if funcion_flecha.group(3) else "None"
            parametros = [param.strip().split(':')[0] for param in parametros]  # Limpiar espacios y extraer solo el nombre del parámetro
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': return_type}

            funciones_globales.append(funcion_con_parametros)
            continue

        # ------------------------------------ Buscar return usando regex
        retorno = re.search(regex_return, linea)
        if retorno and funcion_con_parametros:
            valor_retorno = retorno.group(1).strip()
            funcion_con_parametros['return'] = valor_retorno  # Solo guardar el valor de retorno

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
    # Código TypeScript a analizar
    codigo_typescript = """
    class Test {
        add(a: number, b: number): number {
            return a + b;
        }

        printHello(): void {
            console.log("Hello World");
        }
    }

    class AnotherClass {
        getName(): string {
            return "MyName";
        }

        log(message: string): boolean {
            if (a === 1) { return false; }
            return true;
        }
    }

    // Función global
    function multiply(x: number, y: number): number {
        return x * y;
    }

    // Arrow function
    const divide = (x: number, y: number): number => {
        return x / y;
    };
    """  # Código TypeScript que deseas analizar

    # Llamamos a la función y obtenemos los resultados
    clases_info, funciones_info = extract_info(codigo_typescript)

    # Mostramos los resultados
    print("Clases y funciones encontradas:")
    print(clases_info)
    print("Funciones globales encontradas:")
    print(funciones_info)

    # Definir la salida esperada
    salida_esperada_clases = {
        'Test': [
            {'name': 'add', 'params': ['a', 'b'], 'return': 'number'},
            {'name': 'printHello', 'params': [], 'return': 'void'}
        ],
        'AnotherClass': [
            {'name': 'getName', 'params': [], 'return': 'string'},
            {'name': 'log', 'params': ['message'], 'return': 'boolean'}
        ]
    }

    salida_esperada_globales = [
        {'name': 'multiply', 'params': ['x', 'y'], 'return': 'number'},  # Agregado 'multiply' a la salida esperada
        {'name': 'divide', 'params': ['x', 'y'], 'return': 'number'}
    ]

    # Comprobamos que los resultados coincidan con la salida esperada
    if clases_info == salida_esperada_clases and funciones_info == salida_esperada_globales:
        print("Prueba exitosa: Los resultados son los esperados.")
    else:
        print("Prueba fallida: Los resultados no coinciden con lo esperado.")
