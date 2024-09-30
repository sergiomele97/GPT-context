import re


def extract_info(codigo_ruby):
    # --------------------------------------------------------------------------------------------------- Parámetros

    # ---REGEX---------
    regex_imports = r'^\s*require\s+["\']([^"\']+)["\']'  # Captura los imports
    regex_clases = r'class\s+([A-Za-z_][A-Za-z0-9_]*)'
    regex_funciones_clase = r'^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)'  # Captura función dentro de clase
    regex_funciones_globales = r'^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)'  # Captura función global
    regex_return = r'^\s*return\s+([^;]+)'  # Capturar retorno

    # ---OUTPUT--------
    clases_y_funciones = {}
    funciones_globales = []
    imports_info = []  # Lista para almacenar los imports

    # ---VARIABLES-----
    clase_actual = None

    # ------------------------------------------------------------------------------------------ Lectura línea a línea
    lineas = codigo_ruby.splitlines()

    for linea in lineas:
        linea = linea.strip()  # Limpiar espacios en blanco al inicio y al final

        # ----------------------------------- Buscar imports
        import_match = re.search(regex_imports, linea)
        if import_match:
            imports_info.append(import_match.group(1))  # Agregar el import a la lista
            continue

        # ----------------------------------- Buscar clases
        clase = re.search(regex_clases, linea)
        if clase:
            clase_actual = clase.group(1)
            clases_y_funciones[clase_actual] = []  # Inicializar la lista de funciones para esta clase
            continue

        # ------------------------------------ Buscar funciones en clase
        funcion_clase = re.search(regex_funciones_clase, linea)
        if funcion_clase:
            nombre_funcion = funcion_clase.group(1)
            parametros = funcion_clase.group(2).split(',') if funcion_clase.group(2).strip() else []
            parametros = [param.strip() for param in parametros]  # Limpiar espacios

            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': ''}
            clases_y_funciones[clase_actual].append(funcion_con_parametros)
            continue

        # ------------------------------------ Buscar funciones globales
        funcion_global = re.search(regex_funciones_globales, linea)
        if funcion_global and clase_actual is None:
            nombre_funcion = funcion_global.group(1)
            parametros = funcion_global.group(2).split(',') if funcion_global.group(2).strip() else []
            parametros = [param.strip() for param in parametros]  # Limpiar espacios

            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': ''}
            funciones_globales.append(funcion_con_parametros)

        # ------------------------------------ Buscar return usando regex
        retorno = re.search(regex_return, linea)
        if retorno:
            valor_retorno = retorno.group(1).strip()
            if clase_actual and clases_y_funciones[clase_actual]:
                # Última función añadida a la clase
                if not clases_y_funciones[clase_actual][-1]['return']:
                    clases_y_funciones[clase_actual][-1]['return'] = valor_retorno
                else:
                    clases_y_funciones[clase_actual][-1]['return'] += f"; {valor_retorno}"
            elif not clase_actual and funciones_globales:
                # Última función global añadida
                if not funciones_globales[-1]['return']:
                    funciones_globales[-1]['return'] = valor_retorno
                else:
                    funciones_globales[-1]['return'] += f"; {valor_retorno}"

    # --- Formatear la salida en el formato requerido
    clases_info = {clase: [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones]
                   for clase, funciones in clases_y_funciones.items()}
    funciones_info = [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones_globales]

    return imports_info, clases_info, funciones_info


# ---------------------------------------------------------------------------------------------------------- TESTING
if __name__ == "__main__":
    # Código Ruby que deseas analizar
    codigo_ruby = """
    require 'some_library'
    class Test
        def add(a, b)
            return a + b
        end

        def print_hello
            puts "Hello World"
            return
        end
    end

    class AnotherClass
        def get_name
            return "MyName"
        end

        private
        def log(message)
            if a == 1
                return false
            else
                return true
            end
            puts message
        end
    end

    # Esta es una función global
    def multiply(x, y)
        return x * y
    end
    """  # Código Ruby que deseas analizar

    # Llamamos a la función y obtenemos los resultados
    imports_info, clases_info, funciones_info = extract_info(codigo_ruby)

    # Mostramos los resultados
    print("Imports encontrados:")
    print(imports_info)
    print("Clases y funciones encontradas:")
    print(clases_info)
    print("Funciones globales encontradas:")
    print(funciones_info)

    # Definir la salida esperada
    salida_esperada_imports = ['some_library']

    salida_esperada_clases = {
        'Test': [
            {'name': 'add', 'params': ['a', 'b'], 'return': 'a + b'},
            {'name': 'print_hello', 'params': [], 'return': ''}
        ],
        'AnotherClass': [
            {'name': 'get_name', 'params': [], 'return': '"MyName"'},
            {'name': 'log', 'params': ['message'], 'return': 'false; true'}
        ]
    }

    salida_esperada_globales = [
        {'name': 'multiply', 'params': ['x', 'y'], 'return': 'x * y'}
    ]

    # Comprobamos que los resultados coincidan con la salida esperada
    if imports_info == salida_esperada_imports and clases_info == salida_esperada_clases and funciones_info == salida_esperada_globales:
        print("Prueba exitosa: Los resultados son los esperados.")
    else:
        print("Prueba fallida: Los resultados no coinciden con lo esperado.")
