import re


def extract_info(codigo_go):
    # --------------------------------------------------------------------------------------------------- Parámetros

    # ---REGEX---------
    regex_structs = r'type\s+([A-Za-z_][A-Za-z0-9_]*)\s+struct\s*{'
    regex_funciones = r'func\s+(?:\([A-Za-z_][A-Za-z0-9_]*\s*\*\w+\)\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*(?:\w+)?\s*{'
    regex_return = r'return\s+([^;]+);?'  # Capturar el valor después del 'return'

    # ---OUTPUT--------
    structs_y_funciones = {}
    funciones_globales = []

    # ---VARIABLES-----
    struct_actual = None
    llaves_abiertas = 0  # Contador de {}
    funcion_con_parametros = None  # Inicializamos aquí

    # ------------------------------------------------------------------------------------------ Lectura linea a linea
    lineas = codigo_go.splitlines()

    for linea in lineas:
        llaves_abiertas += linea.count('{') - linea.count('}')

        # ----------------------------------- Buscar structs
        struct = re.search(regex_structs, linea)
        if struct:
            struct_actual = struct.group(1)
            structs_y_funciones[struct_actual] = []  # Inicializar la lista de funciones para este struct
            continue

        # ------------------------------------ Buscar funciones
        funcion = re.search(regex_funciones, linea)
        if funcion:
            nombre_funcion = funcion.group(1)
            parametros = funcion.group(2).split(',') if funcion.group(2).strip() else []
            parametros = [param.strip() for param in parametros]  # Limpiar espacios
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': ''}

            if struct_actual:  # Si estamos dentro de un struct
                structs_y_funciones[struct_actual].append(funcion_con_parametros)
            else:
                # Si no estamos dentro de un struct, es una función global
                funciones_globales.append(funcion_con_parametros)

        # ------------------------------------ Buscar return usando regex
        retorno = re.search(regex_return, linea)
        if retorno and funcion_con_parametros:  # Verificar que funcion_con_parametros está inicializada
            valor_retorno = retorno.group(1).strip()
            if funcion_con_parametros['return']:
                funcion_con_parametros['return'] += f"; {valor_retorno}"  # Añadir con separación
            else:
                funcion_con_parametros['return'] = valor_retorno  # Almacenar solo el valor de retorno

        # Si las llaves llegan a 0, salimos del struct
        if llaves_abiertas == 0:
            struct_actual = None

    # --- Formatear la salida en el formato requerido
    structs_info = {struct: [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones]
                    for struct, funciones in structs_y_funciones.items()}
    funciones_info = [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones_globales]

    return structs_info, funciones_info

# ---------------------------------------------------------------------------------------------------------- TESTING
if __name__ == "__main__":
    # Código Go para probar
    codigo_go = """
    package main

    import "fmt"

    type Test struct {
        // Campos de prueba
    }

    func (t *Test) Add(a int, b int) int {
        return a + b
    }

    func (t *Test) PrintHello() {
        fmt.Println("Hello World")
        return  // No tiene valor de retorno
    }

    type AnotherStruct struct {
        // Campos de prueba
    }

    func (as *AnotherStruct) GetName() string {
        return "MyName"
    }

    func (as *AnotherStruct) Log(message string) bool {
        if a == 1 {
            return false
        } else {
            return true
        }
        fmt.Println(message)
    }

    // Esta es una función global
    func Multiply(x int, y int) int {
        return x * y
    }
    """  # Código Go que deseas analizar

    # Llamamos a la función y obtenemos los resultados
    structs_info, funciones_info = extract_info(codigo_go)

    # Mostramos los resultados
    print("Structs y funciones encontradas:")
    print(structs_info)
    print("Funciones globales encontradas:")
    print(funciones_info)

    # Definir la salida esperada
    salida_esperada_structs = {
        'Test': [
            {'name': 'Add', 'params': ['a int', 'b int'], 'return': 'a + b'},
            {'name': 'PrintHello', 'params': [], 'return': ''}
        ],
        'AnotherStruct': [
            {'name': 'GetName', 'params': [], 'return': '"MyName"'},
            {'name': 'Log', 'params': ['message string'], 'return': 'false; true'}
        ]
    }

    salida_esperada_globales = [
        {'name': 'Multiply', 'params': ['x int', 'y int'], 'return': 'x * y'}
    ]

    # Comprobamos que los resultados coincidan con la salida esperada
    if structs_info == salida_esperada_structs and funciones_info == salida_esperada_globales:
        print("Prueba exitosa: Los resultados son los esperados.")
    else:
        print("Prueba fallida: Los resultados no coinciden con lo esperado.")
