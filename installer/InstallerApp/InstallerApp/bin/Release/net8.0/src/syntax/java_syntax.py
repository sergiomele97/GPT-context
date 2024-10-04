import re

def extract_info(codigo_java):
    # --------------------------------------------------------------------------------------------------- Parámetros

    # ---REGEX---------
    regex_imports = r'import\s+([A-Za-z0-9_.]+);'  # Captura los imports
    regex_clases = r'class\s+([A-Za-z_][A-Za-z0-9_]*)'
    regex_funciones = r'(public|private|protected|static|final|void)\s+([A-Za-z_][A-Za-z0-9_<>]*)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)'
    regex_return = r'return\s+([^;]+);?'  # Capturar el valor después del 'return'

    # ---OUTPUT--------
    clases_y_funciones = {}
    funciones_globales = []
    imports_info = []  # Nueva lista para almacenar los imports

    # ---VARIABLES-----
    clase_actual = None
    llaves_abiertas = 0  # Contador de {}
    funcion_con_parametros = None  # Inicializar aquí para evitar el error

    # ------------------------------------------------------------------------------------------ Lectura linea a linea
    lineas = codigo_java.splitlines()

    for linea in lineas:
        # Buscar imports
        importacion = re.search(regex_imports, linea)
        if importacion:
            imports_info.append(importacion.group(1))
            continue  # Continuar sin procesar más la línea si se encontró un import

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
            nombre_funcion = funcion.group(3)
            parametros = funcion.group(4).split(',') if funcion.group(4).strip() else []
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

    return imports_info, clases_info, funciones_info

# ---------------------------------------------------------------------------------------------------------- TESTING
if __name__ == "__main__":
    # Código Java para analizar
    codigo_java = """
    import java.util.List;
    import java.util.ArrayList;

    public class Test {
        public int add(int a, int b) {
            return a + b;
        }

        public void printHello() {
            System.out.println("Hello World");
            return;  // No tiene valor de retorno
        }
    }

    public class AnotherClass {
        public String getName() {
            return "MyName";
        }

        private boolean log(String message) {
            if (a == 1) { return false; }
            else { return true; }
            System.out.println(message);
        }
    }

    // Esta es una función global
    public int multiply(int x, int y) {
        return x * y;
    }
    """  # Código Java que deseas analizar

    # Llamamos a la función y obtenemos los resultados
    imports_info, clases_info, funciones_info = extract_info(codigo_java)

    # Mostramos los resultados
    print("Imports encontrados:")
    print(imports_info)
    print("Clases y funciones encontradas:")
    print(clases_info)
    print("Funciones globales encontradas:")
    print(funciones_info)

    # Definir la salida esperada
    salida_esperada_imports = [
        'java.util.List',
        'java.util.ArrayList'
    ]

    salida_esperada_clases = {
        'Test': [
            {'name': 'add', 'params': ['int a', 'int b'], 'return': 'a + b'},
            {'name': 'printHello', 'params': [], 'return': ''}
        ],
        'AnotherClass': [
            {'name': 'getName', 'params': [], 'return': '"MyName"'},
            {'name': 'log', 'params': ['String message'], 'return': 'false; true'}
        ]
    }

    salida_esperada_globales = [
        {'name': 'multiply', 'params': ['int x', 'int y'], 'return': 'x * y'}
    ]

    # Comprobamos que los resultados coincidan con la salida esperada
    if imports_info == salida_esperada_imports and clases_info == salida_esperada_clases and funciones_info == salida_esperada_globales:
        print("Prueba exitosa: Los resultados son los esperados.")
    else:
        print("Prueba fallida: Los resultados no coinciden con lo esperado.")
