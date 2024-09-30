import re

def extract_functions_and_classes(codigo_cpp):
    # ---REGEX---------
    regex_clases = r'class\s+([A-Za-z_][A-Za-z0-9_]*)\s*{'
    regex_funciones = r'\b(public|private|protected|virtual|inline)?\s*[A-Za-z_][A-Za-z0-9_<>]*\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*{'
    regex_return = r'return\s+([^;]+);?'  # Capturar el valor después del 'return'

    # ---OUTPUT--------
    clases_y_funciones = {}
    funciones_globales = []

    # ---VARIABLES-----
    clase_actual = None
    llaves_abiertas = 0  # Contador de {}
    funcion_con_parametros = None  # Inicializar aquí para evitar el error

    # ------------------------------------------------------------------------------------------ Lectura linea a linea
    lineas = codigo_cpp.splitlines()

    for linea in lineas:
        # Actualizar el contador de llaves
        llaves_abiertas += linea.count('{') - linea.count('}')

        # ----------------------------------- Buscar clases
        clase = re.search(regex_clases, linea)
        if clase:
            clase_actual = clase.group(1)
            clases_y_funciones[clase_actual] = []  # Inicializar la lista de funciones para esta clase
            continue

        # ------------------------------------ Buscar funciones
        funcion = re.search(regex_funciones, linea)
        if funcion:
            nombre_funcion = funcion.group(2)
            parametros = funcion.group(3).split(',') if funcion.group(3).strip() else []
            parametros = [param.strip() for param in parametros]  # Limpiar espacios
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': ''}

            if clase_actual:
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
    # Código C++ de ejemplo
    codigo_cpp = """
    class Test {
    public:
        int Add(int a, int b) {
            return a + b;
        }

        void PrintHello() {
            std::cout << "Hello World" << std::endl;
            return;  // No tiene valor de retorno
        }
    };

    class AnotherClass {
    public:
        std::string GetName() {
            return "MyName";
        }

    private:
        void Log(std::string message) {
            if (a == 1) { return false; }
            else { return true; }
            std::cout << message;
        }
    };

    // Esta es una función global
    int Multiply(int x, int y) {
        return x * y;
    }
    """  # Código C++ que deseas analizar

    # Llamamos a la función y obtenemos los resultados
    clases_info, funciones_info = extract_functions_and_classes(codigo_cpp)

    # Mostramos los resultados
    print("Clases y funciones encontradas:")
    print(clases_info)
    print("Funciones globales encontradas:")
    print(funciones_info)

    # Definir la salida esperada
    salida_esperada_clases = {
        'Test': [
            {'name': 'Add', 'params': ['int a', 'int b'], 'return': 'a + b'},
            {'name': 'PrintHello', 'params': [], 'return': ''}
        ],
        'AnotherClass': [
            {'name': 'GetName', 'params': [], 'return': '"MyName"'},
            {'name': 'Log', 'params': ['std::string message'], 'return': 'false; true'}
        ]
    }

    salida_esperada_globales = [
        {'name': 'Multiply', 'params': ['int x', 'int y'], 'return': 'x * y'}
    ]

    # Comprobamos que los resultados coincidan con la salida esperada
    if clases_info == salida_esperada_clases and funciones_info == salida_esperada_globales:
        print("Prueba exitosa: Los resultados son los esperados.")
    else:
        print("Prueba fallida: Los resultados no coinciden con lo esperado.")
