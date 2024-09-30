import re

def extract_info(codigo_php):
    # ---REGEX---------
    regex_imports = r'use\s+([A-Za-z0-9_\\]+(?:\\\\[A-Za-z0-9_]+)*);'  # Para detectar imports
    regex_clases = r'class\s+([A-Za-z_][A-Za-z0-9_]*)'
    regex_funciones = r'(public|private|protected|static)\s+function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)'
    regex_funciones_globales = r'function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)'  # Funciones globales sin modificadores
    regex_return = r'return\s+([^;]+);?'  # Capturar el valor después del 'return'

    # ---OUTPUT--------
    imports_info = []  # Lista para almacenar imports
    clases_y_funciones = {}
    funciones_globales = []

    # ---VARIABLES-----
    clase_actual = None
    llaves_abiertas = 0  # Contador de {}

    # ------------------------------------------------------------------------------------------ Lectura línea a línea
    lineas = codigo_php.splitlines()

    for linea in lineas:
        # Buscar imports
        import_match = re.search(regex_imports, linea)
        if import_match:
            imports_info.append(import_match.group(1))  # Añadir import a la lista
            continue

        llaves_abiertas += linea.count('{') - linea.count('}')

        # ----------------------------------- Buscar clases
        clase = re.search(regex_clases, linea)
        if clase:
            clase_actual = clase.group(1)
            clases_y_funciones[clase_actual] = []  # Inicializar la lista de funciones para esta clase
            llaves_abiertas = 1
            continue

        # ------------------------------------ Buscar funciones dentro de clases
        funcion = re.search(regex_funciones, linea)
        if funcion:
            nombre_funcion = funcion.group(2)
            parametros = funcion.group(3).split(',') if funcion.group(3).strip() else []
            parametros = [param.strip() for param in parametros]  # Limpiar espacios
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': ''}

            # Si estamos dentro de una clase, agregamos la función a esa clase
            if clase_actual:
                clases_y_funciones[clase_actual].append(funcion_con_parametros)
            continue  # Saltar a la siguiente línea

        # ------------------------------------ Buscar funciones globales
        funcion_global = re.search(regex_funciones_globales, linea)
        if funcion_global:
            nombre_funcion_global = funcion_global.group(1)
            parametros_globales = funcion_global.group(2).split(',') if funcion_global.group(2).strip() else []
            parametros_globales = [param.strip() for param in parametros_globales]
            funcion_global_con_parametros = {'name': nombre_funcion_global, 'params': parametros_globales, 'return': ''}
            funciones_globales.append(funcion_global_con_parametros)

        # ------------------------------------ Buscar return usando regex
        retorno = re.search(regex_return, linea)
        if retorno:
            valor_retorno = retorno.group(1).strip()
            # Verificar si estamos en el contexto de una clase o global
            if clase_actual and clases_y_funciones[clase_actual]:
                # Almacenar el retorno en la última función de la clase
                clases_y_funciones[clase_actual][-1]['return'] += valor_retorno + '; '  # Añadir con separación
            elif funciones_globales:
                # Almacenar el retorno en la última función global
                funciones_globales[-1]['return'] += valor_retorno + '; '

        # Si las llaves llegan a 0, salimos de la clase
        if llaves_abiertas == 0:
            clase_actual = None

    # --- Formatear la salida en el formato requerido
    clases_info = {clase: [{'name': f['name'], 'params': f['params'], 'return': f['return'].strip('; ')} for f in funciones]
                   for clase, funciones in clases_y_funciones.items()}
    funciones_info = [{'name': f['name'], 'params': f['params'], 'return': f['return'].strip('; ')} for f in funciones_globales]

    return imports_info, clases_info, funciones_info


# ---------------------------------------------------------------------------------------------------------- TESTING
if __name__ == "__main__":
    # Código PHP de ejemplo
    codigo_php = """
    use Some\\Namespace\\Class;
    use Another\\Namespace\\Function;

    class Test {
        public function add($a, $b) {
            return $a + $b;
        }

        public function printHello() {
            echo "Hello World";
            return;  // No tiene valor de retorno
        }
    }

    class AnotherClass {
        public function getName() {
            return "MyName";
        }

        private function log($message) {
            if($a == 1) { return false; }
            else { return true; }
            echo $message;
        }
    }

    // Esta es una función global
    function multiply($x, $y) {
        return $x * $y;
    }
    """  # Código PHP que deseas analizar

    # Llamamos a la función y obtenemos los resultados
    imports_info, clases_info, funciones_info = extract_info(codigo_php)

    # Mostramos los resultados
    print("Imports encontrados:")
    print(imports_info)
    print("Clases y funciones encontradas:")
    print(clases_info)
    print("Funciones globales encontradas:")
    print(funciones_info)

    # Definir la salida esperada
    salida_esperada_imports = [
        'Some\\Namespace\\Class',
        'Another\\Namespace\\Function'
    ]

    salida_esperada_clases = {
        'Test': [
            {'name': 'add', 'params': ['$a', '$b'], 'return': '$a + $b'},
            {'name': 'printHello', 'params': [], 'return': ''}  # Se agrega printHello a la salida esperada
        ],
        'AnotherClass': [
            {'name': 'getName', 'params': [], 'return': '"MyName"'},
            {'name': 'log', 'params': ['$message'], 'return': 'false; true'}
        ]
    }

    salida_esperada_globales = [
        {'name': 'multiply', 'params': ['$x', '$y'], 'return': '$x * $y'}
    ]

    # Comprobamos que los resultados coincidan con la salida esperada
    if imports_info == salida_esperada_imports and clases_info == salida_esperada_clases and funciones_info == salida_esperada_globales:
        print("Prueba exitosa: Los resultados son los esperados.")
    else:
        print("Prueba fallida: Los resultados no coinciden con lo esperado.")
