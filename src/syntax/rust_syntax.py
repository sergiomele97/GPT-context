import re

def extract_info(codigo_rust):
    # --------------------------------------------------------------------------------------------------- Parámetros

    # ---REGEX---------
    regex_structs = r'struct\s+([A-Za-z_][A-Za-z0-9_]*)'
    regex_funciones = r'(?:pub\s+)?fn\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*(->\s*([A-Za-z_][A-Za-z0-9_<>]*))?'
    regex_return = r'return\s+([^;]+);'  # Capturar el valor después del 'return'

    # ---OUTPUT--------
    structs_y_funciones = {}
    funciones_globales = []

    # ---VARIABLES-----
    struct_actual = None
    llaves_abiertas = 0  # Contador de {}
    dentro_de_impl = False  # Para saber si estamos dentro de un bloque impl
    funcion_con_parametros = None  # Inicializar aquí para evitar el error

    # ------------------------------------------------------------------------------------------ Lectura linea a linea
    lineas = codigo_rust.splitlines()

    for linea in lineas:
        llaves_abiertas += linea.count('{') - linea.count('}')

        # ----------------------------------- Detectar el comienzo de un impl para un struct
        if 'impl' in linea:
            dentro_de_impl = True
            continue

        # ----------------------------------- Detectar el fin de un impl
        if llaves_abiertas == 0 and dentro_de_impl:
            dentro_de_impl = False
            struct_actual = None  # Ya no estamos en un struct

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
            tipo_retorno = funcion.group(4) if funcion.group(4) else '()'  # Si no hay retorno explícito, es `()`
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': tipo_retorno}

            if dentro_de_impl and struct_actual:
                # Si estamos dentro de un impl (es decir, dentro de un struct)
                structs_y_funciones[struct_actual].append(funcion_con_parametros)
            else:
                # Si no estamos dentro de un struct, es una función global
                funciones_globales.append(funcion_con_parametros)

        # ------------------------------------ Buscar return usando regex
        retorno = re.search(regex_return, linea)
        if retorno and funcion_con_parametros:  # Verificar que funcion_con_parametros está inicializada
            valor_retorno = retorno.group(1).strip()
            if funcion_con_parametros['return'] != '()':  # Si ya hay un retorno
                funcion_con_parametros['return'] += f"; {valor_retorno}"  # Añadir con separación
            else:
                funcion_con_parametros['return'] = valor_retorno  # Almacenar solo el valor de retorno

    # --- Formatear la salida en el formato requerido
    structs_info = {struct: [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones]
                   for struct, funciones in structs_y_funciones.items()}
    funciones_info = [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones_globales]

    return structs_info, funciones_info


# ---------------------------------------------------------------------------------------------------------- TESTING
if __name__ == "__main__":
    # Código Rust que deseas analizar
    codigo_rust = """
    struct Test;

    impl Test {
        pub fn add(a: i32, b: i32) -> i32 {
            return a + b;
        }

        fn print_hello() {
            println!("Hello, world!");
        }
    }

    struct AnotherStruct;

    impl AnotherStruct {
        pub fn get_name() -> &'static str {
            return "MyName";
        }

        fn log(message: &str) -> bool {
            if true {
                return false;
            }
            println!("{}", message);
            true
        }
    }

    // Esta es una función global
    pub fn multiply(x: i32, y: i32) -> i32 {
        x * y
    }
    """

    # Llamamos a la función y obtenemos los resultados
    structs_info, funciones_info = extract_info(codigo_rust)

    # Mostramos los resultados
    print("Structs y funciones encontradas:")
    print(structs_info)
    print("Funciones globales encontradas:")
    print(funciones_info)

    # Definir la salida esperada
    salida_esperada_structs = {
        'Test': [
            {'name': 'add', 'params': ['a: i32', 'b: i32'], 'return': 'a + b'},
            {'name': 'print_hello', 'params': [], 'return': '()'}
        ],
        'AnotherStruct': [
            {'name': 'get_name', 'params': [], 'return': '"MyName"'},
            {'name': 'log', 'params': ['message: &str'], 'return': 'false; true'}
        ]
    }

    salida_esperada_globales = [
        {'name': 'multiply', 'params': ['x: i32', 'y: i32'], 'return': 'x * y'}
    ]

    # Comprobamos que los resultados coincidan con la salida esperada
    if structs_info == salida_esperada_structs and funciones_info == salida_esperada_globales:
        print("Prueba exitosa: Los resultados son los esperados.")
    else:
        print("Prueba fallida: Los resultados no coinciden con lo esperado.")
