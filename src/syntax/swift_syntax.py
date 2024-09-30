import re

def extract_info(codigo_swift):
    # --------------------------------------------------------------------------------------------------- Parámetros

    # ---REGEX---------
    regex_imports = r'import\s+(\w+)'  # Detecta un import en Swift
    regex_clases = r'class\s+(\w+)'  # Detecta una clase en Swift
    regex_funciones = r'func\s+(\w+)\s*\((.*?)\)\s*(->\s*(\w+))?\s*{'  # Detecta una función en Swift
    regex_return = r'return\s+(.*?)(;|$)'  # Detecta un retorno en una función

    # ---OUTPUT--------
    imports_info = []  # Inicializar lista de imports
    clases_y_funciones = {}
    funciones_globales = []

    # ---VARIABLES-----
    estamos_dentro_de_una_clase = False
    funcion_con_parametros = None  # Para guardar la función actual

    # ------------------------------------------------------------------------------------------ Lectura linea a linea
    lineas = codigo_swift.splitlines()

    for linea in lineas:
        # ----------------------------------- Buscar imports
        importacion = re.search(regex_imports, linea)
        if importacion:  # detectamos un import
            imports_info.append(importacion.group(1))  # Añadir el nombre del módulo importado
            continue

        # ----------------------------------- Buscar clases
        clase = re.search(regex_clases, linea)
        if clase:  # detectamos una clase
            estamos_dentro_de_una_clase = True
            clase_actual = clase.group(1)
            clases_y_funciones[clase_actual] = []  # Inicializar la lista de funciones para esta clase
            continue

        # ------------------------------------ Buscar funciones
        funcion = re.search(regex_funciones, linea)
        if funcion:  # detectamos una función
            nombre_funcion = funcion.group(1)
            parametros = funcion.group(2).split(',') if funcion.group(2).strip() else []
            parametros = [param.strip() for param in parametros]  # Limpiar espacios
            return_type = funcion.group(4) if funcion.group(4) else ''  # Tipo de retorno

            # Crear un diccionario para la función
            funcion_con_parametros = {
                'name': nombre_funcion,
                'params': parametros,
                'return': return_type  # Guardar el tipo de retorno
            }

            if estamos_dentro_de_una_clase:
                # Si estamos dentro de una clase, agregamos la función a esa clase
                clases_y_funciones[clase_actual].append(funcion_con_parametros)
            else:
                # Si no estamos dentro de una clase, es una función global
                funciones_globales.append(funcion_con_parametros)

        # ------------------------------------ Buscar return usando regex
        retorno = re.search(regex_return, linea)
        if retorno and funcion_con_parametros:  # Verificar que funcion_con_parametros está inicializada
            # Añadimos el valor de retorno a la función actual
            funcion_con_parametros['return'] = retorno.group(1).strip()  # Capturamos el valor de retorno

        # ------------------------------------ Detectar el fin de una clase
        if linea.strip() == '}':
            estamos_dentro_de_una_clase = False

    # --- Formatear la salida en el formato requerido
    clases_info = {clase: [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones]
                   for clase, funciones in clases_y_funciones.items()}
    funciones_info = [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones_globales]

    return imports_info, clases_info, funciones_info


# ---------------------------------------------------------------------------------------------------------- TESTING
if __name__ == "__main__":
    # Código Swift que deseas analizar
    codigo_swift = """
    import Foundation
    import UIKit

    class Test {
        func add(a: Int, b: Int) -> Int {
            return a + b
        }

        func printHello() {
            print("Hello World")
            return  
        }
    }

    class AnotherClass {
        func getName() -> String {
            return "MyName"
        }

        private func log(message: String) {
            if a == 1 { return false }
            else { return true }
            print(message)
        }
    }

    // Esta es una función global
    func multiply(x: Int, y: Int) -> Int {
        return x * y
    }
    """  # Código Swift que deseas analizar

    # Llamamos a la función y obtenemos los resultados
    imports_info, clases_info, funciones_info = extract_info(codigo_swift)

    # Mostramos los resultados
    print("Imports encontrados:")
    print(imports_info)
    print("Clases y funciones encontradas:")
    print(clases_info)
    print("Funciones globales encontradas:")
    print(funciones_info)

    # Definir la salida esperada
    salida_esperada_imports = ['Foundation', 'UIKit']
    salida_esperada_clases = {
        'Test': [
            {'name': 'add', 'params': ['a: Int', 'b: Int'], 'return': 'Int'},
            {'name': 'printHello', 'params': [], 'return': ''}
        ],
        'AnotherClass': [
            {'name': 'getName', 'params': [], 'return': 'String'},
            {'name': 'log', 'params': ['message: String'], 'return': 'Bool'}  # Cambiado a Bool
        ]
    }

    salida_esperada_globales = [
        {'name': 'multiply', 'params': ['x: Int', 'y: Int'], 'return': 'Int'}
    ]

    # Comprobamos que los resultados coincidan con la salida esperada
    if imports_info == salida_esperada_imports and clases_info == salida_esperada_clases and funciones_info == salida_esperada_globales:
        print("Prueba exitosa: Los resultados son los esperados.")
    else:
        print("Prueba fallida: Los resultados no coinciden con lo esperado.")
