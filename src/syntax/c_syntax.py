import re

def extract_info(codigo_c):
    # --------------------------------------------------------------------------------------------------- Parameters

    # ---REGEX---------
    # C does not have classes, so we remove class analysis
    regex_funciones = r'([a-zA-Z_][a-zA-Z0-9_*\s]*?)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*\{'
    regex_return = r'return\s+([^;]+);'  # Capture the value after 'return'
    regex_imports = r'^\s*#include\s*<([^>]+)>'  # Capture library imports

    # ---OUTPUT--------
    funciones_globales = []
    imports_globales = []

    # ---VARIABLES-----
    funcion_con_parametros = None

    # ------------------------------------------------------------------------------------------ Read line by line
    lineas = codigo_c.splitlines()

    for linea in lineas:
        # ------------------------------------ Search for imports
        importacion = re.search(regex_imports, linea)
        if importacion:
            imports_globales.append(importacion.group(1).strip())  # Store the name of the imported file

        # ------------------------------------ Search for functions
        funcion = re.search(regex_funciones, linea)
        if funcion:
            tipo_retorno = funcion.group(1).strip()  # Capture the return type
            nombre_funcion = funcion.group(2).strip()  # Capture the function name
            parametros = funcion.group(3).split(',') if funcion.group(3).strip() else []  # Capture parameters
            parametros = [param.strip() for param in parametros]  # Clean spaces
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return_type': tipo_retorno, 'return': ''}

            # Store the function globally
            funciones_globales.append(funcion_con_parametros)

        # ------------------------------------ Search for return using regex
        retorno = re.search(regex_return, linea)
        if retorno and funcion_con_parametros:  # Check that funcion_con_parametros is initialized
            valor_retorno = retorno.group(1).strip()
            if funcion_con_parametros['return']:
                funcion_con_parametros['return'] += f"; {valor_retorno}"  # Add with separation
            else:
                funcion_con_parametros['return'] = valor_retorno  # Store only the return value

    # --- Format the output in the required format
    funciones_info = [{'name': f['name'], 'params': f['params'], 'return_type': f['return_type'], 'return': f['return']} for f in funciones_globales]

    return {'imports': imports_globales, 'classes': [], 'functions': funciones_info}  # Returns imports, classes (empty), and functions


# ---------------------------------------------------------------------------------------------------------- TESTING
if __name__ == "__main__":
    # Example C code
    codigo_c = """
    #include <stdio.h>
    #include <stdlib.h>

    int suma(int a, int b) {
        return a + b;
    }

    void imprimeMensaje() {
        printf("Hello World");
        return;
    }

    float calcularPromedio(float num1, float num2) {
        float resultado = (num1 + num2) / 2;
        return resultado;
    }
    """

    # Call the function and get the results
    resultados = extract_info(codigo_c)

    # Display the results
    print("Imports found:")
    print(resultados['imports'])
    print("Classes found (empty):")
    print(resultados['classes'])
    print("Global functions found:")
    print(resultados['functions'])

    # Define the expected output
    salida_esperada_globales = [
        {'name': 'suma', 'params': ['int a', 'int b'], 'return_type': 'int', 'return': 'a + b'},
        {'name': 'imprimeMensaje', 'params': [], 'return_type': 'void', 'return': ''},
        {'name': 'calcularPromedio', 'params': ['float num1', 'float num2'], 'return_type': 'float', 'return': 'resultado'}
    ]
    salida_esperada_imports = ['stdio.h', 'stdlib.h']

    # Check that the results match the expected output
    if resultados['functions'] == salida_esperada_globales and resultados['imports'] == salida_esperada_imports:
        print("Test successful: The results are as expected.")
    else:
        print("Test failed: The results do not match the expected output.")
