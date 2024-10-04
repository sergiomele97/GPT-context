import re

def extract_info(codigo_javascript):
    # --------------------------------------------------------------------------------------------------- Parámetros

    # ---REGEX---------
    regex_imports = r'import\s+[\w\s{},*]+\s+from\s+["\'][\w/\-.]+["\']'  # Regex para detectar imports
    regex_clases = r'class\s+([A-Za-z_][A-Za-z0-9_]*)'
    regex_funciones_clase = r'([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*\{'
    regex_funciones_globales = r'function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*\{'
    regex_arrow_functions = r'const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\(([^)]*)\)\s*=>\s*\{'
    regex_return = r'return\s+([^;]+);?'  # Capturar el valor después del 'return'
    # Ignorar bloques como if, for, while
    regex_control_blocks = r'\b(if|else|for|while|switch|catch|try|finally)\b'

    # ---OUTPUT--------
    imports_info = []  # Lista para almacenar imports
    clases_y_funciones = {}
    funciones_globales = []

    # ---VARIABLES-----
    clase_actual = None
    llaves_abiertas = 0  # Contador de {}
    funcion_con_parametros = None  # Inicializar aquí para evitar el error

    # ------------------------------------------------------------------------------------------ Lectura línea a línea
    lineas = codigo_javascript.splitlines()

    for linea in lineas:
        # Ignorar líneas vacías
        if not linea.strip():
            continue

        # Actualizar el contador de llaves abiertas
        llaves_abiertas += linea.count('{') - linea.count('}')

        # Ignorar bloques de control como if, else, for, etc.
        if re.search(regex_control_blocks, linea):
            continue

        # ----------------------------------- Buscar imports
        importacion = re.search(regex_imports, linea)
        if importacion:
            imports_info.append(importacion.group(0))  # Almacenar la línea del import
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
            parametros = [param.strip() for param in parametros]  # Limpiar espacios
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': "None"}

            if clase_actual and llaves_abiertas > 0:
                clases_y_funciones[clase_actual].append(funcion_con_parametros)
            continue

        # ------------------------------------ Buscar funciones globales (con 'function')
        funcion_global = re.search(regex_funciones_globales, linea)
        if funcion_global:
            nombre_funcion = funcion_global.group(1)
            parametros = funcion_global.group(2).split(',') if funcion_global.group(2).strip() else []
            parametros = [param.strip() for param in parametros]
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': "None"}

            funciones_globales.append(funcion_con_parametros)
            continue

        # ------------------------------------ Buscar funciones flecha (arrow functions)
        funcion_flecha = re.search(regex_arrow_functions, linea)
        if funcion_flecha:
            nombre_funcion = funcion_flecha.group(1)
            parametros = funcion_flecha.group(2).split(',') if funcion_flecha.group(2).strip() else []
            parametros = [param.strip() for param in parametros]
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': "None"}

            funciones_globales.append(funcion_con_parametros)
            continue

        # ------------------------------------ Buscar return usando regex
        retorno = re.search(regex_return, linea)
        if retorno and funcion_con_parametros:
            valor_retorno = retorno.group(1).strip()
            if funcion_con_parametros['return'] == "None":
                funcion_con_parametros['return'] = ""
            funcion_con_parametros['return'] += valor_retorno

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
    codigo_javascript = """
    import { module1, module2 } from 'module-path';
    import defaultExport from 'another-module';

    class Test {
        add(a, b) {
            return a + b;
        }

        printHello() {
            console.log("Hello World");
        }
    }

    class AnotherClass {
        getName() {
            return "MyName";
        }

        log(message) {
            if (a === 1) { return false; }
            return true;
        }
    }

    // Función global
    function multiply(x, y) {
        return x * y;
    }

    // Arrow function
    const divide = (x, y) => {
        return x / y;
    };
    """  # Código JavaScript que deseas analizar

    # Llamamos a la función y obtenemos los resultados
    imports_info, clases_info, funciones_info = extract_info(codigo_javascript)

    # Mostramos los resultados
    print("Imports Info:", imports_info)
    print("Clases Info:", clases_info)
    print("Funciones Info:", funciones_info)
