import re

def extract_info(codigo_c):
    # --------------------------------------------------------------------------------------------------- Parámetros

    # ---REGEX---------
    # C no tiene clases, así que eliminamos el análisis de clases
    regex_funciones = r'([a-zA-Z_][a-zA-Z0-9_*\s]*?)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*\{'
    regex_return = r'return\s+([^;]+);'  # Capturar el valor después del 'return'
    regex_imports = r'^\s*#include\s*<([^>]+)>'  # Capturar imports de bibliotecas

    # ---OUTPUT--------
    funciones_globales = []
    imports_globales = []

    # ---VARIABLES-----
    funcion_con_parametros = None

    # ------------------------------------------------------------------------------------------ Lectura línea a línea
    lineas = codigo_c.splitlines()

    for linea in lineas:
        # ------------------------------------ Buscar imports
        importacion = re.search(regex_imports, linea)
        if importacion:
            imports_globales.append(importacion.group(1).strip())  # Almacena el nombre del archivo importado

        # ------------------------------------ Buscar funciones
        funcion = re.search(regex_funciones, linea)
        if funcion:
            tipo_retorno = funcion.group(1).strip()  # Captura el tipo de retorno
            nombre_funcion = funcion.group(2).strip()  # Captura el nombre de la función
            parametros = funcion.group(3).split(',') if funcion.group(3).strip() else []  # Captura los parámetros
            parametros = [param.strip() for param in parametros]  # Limpiar espacios
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return_type': tipo_retorno, 'return': ''}

            # Guardamos la función globalmente
            funciones_globales.append(funcion_con_parametros)

        # ------------------------------------ Buscar return usando regex
        retorno = re.search(regex_return, linea)
        if retorno and funcion_con_parametros:  # Verificar que funcion_con_parametros está inicializada
            valor_retorno = retorno.group(1).strip()
            if funcion_con_parametros['return']:
                funcion_con_parametros['return'] += f"; {valor_retorno}"  # Añadir con separación
            else:
                funcion_con_parametros['return'] = valor_retorno  # Almacenar solo el valor de retorno

    # --- Formatear la salida en el formato requerido
    funciones_info = [{'name': f['name'], 'params': f['params'], 'return_type': f['return_type'], 'return': f['return']} for f in funciones_globales]

    return {'imports': imports_globales, 'classes': [], 'functions': funciones_info}  # Retorna imports, clases (vacía) y funciones


# ---------------------------------------------------------------------------------------------------------- TESTING
if __name__ == "__main__":
    # Código C de ejemplo
    codigo_c = """
    #include <stdio.h>
    #include <stdlib.h>

    int suma(int a, int b) {
        return a + b;
    }

    void imprimeMensaje() {
        printf("Hola Mundo");
        return;
    }

    float calcularPromedio(float num1, float num2) {
        float resultado = (num1 + num2) / 2;
        return resultado;
    }
    """

    # Llamamos a la función y obtenemos los resultados
    resultados = extract_info(codigo_c)

    # Mostramos los resultados
    print("Imports encontrados:")
    print(resultados['imports'])
    print("Clases encontradas (vacía):")
    print(resultados['classes'])
    print("Funciones globales encontradas:")
    print(resultados['functions'])

    # Definir la salida esperada
    salida_esperada_globales = [
        {'name': 'suma', 'params': ['int a', 'int b'], 'return_type': 'int', 'return': 'a + b'},
        {'name': 'imprimeMensaje', 'params': [], 'return_type': 'void', 'return': ''},
        {'name': 'calcularPromedio', 'params': ['float num1', 'float num2'], 'return_type': 'float', 'return': 'resultado'}
    ]
    salida_esperada_imports = ['stdio.h', 'stdlib.h']

    # Comprobamos que los resultados coincidan con la salida esperada
    if resultados['functions'] == salida_esperada_globales and resultados['imports'] == salida_esperada_imports:
        print("Prueba exitosa: Los resultados son los esperados.")
    else:
        print("Prueba fallida: Los resultados no coinciden con lo esperado.")
