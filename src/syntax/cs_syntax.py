import re

def extraer_clases_y_funciones(codigo_csharp):

    # --------------------------------------------------------------------------------------------------- Parámetros

    global funcion_con_parametros

    # ---REGEX---------
    regex_clases = r'class\s+([A-Za-z_][A-Za-z0-9_]*)'
    regex_funciones = r'(public|private|protected|internal)\s+[A-Za-z_][A-Za-z0-9_<>]*\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)'

    # ---OUTPUT--------
    clases_y_funciones = {}
    funciones_globales = []

    # ---VARIABLES-----
    clase_actual = None
    llaves_abiertas = 0  # Contador de {}


    # ------------------------------------------------------------------------------------------ Lectura linea a linea
    lineas = codigo_csharp.splitlines()

    for linea in lineas:

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

            nombre_funcion = funcion.group(2)
            parametros = funcion.group(3).split(',') if funcion.group(3).strip() else []
            parametros = [param.strip() for param in parametros]  # Limpiar espacios
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': "None"}

            if clase_actual and llaves_abiertas > 0:
                # Si estamos dentro de una clase, agregamos la función a esa clase
                funcion_con_parametros['return'] = ""  # Inicializar retorno
                clases_y_funciones[clase_actual].append(funcion_con_parametros)
            else:
                # Si no estamos dentro de una clase, es una función global
                funcion_con_parametros['return'] = "" # Inicializar retorno
                funciones_globales.append(funcion_con_parametros)

        # ------------------------------------ Buscar return
        if 'return ' in linea:
            # Obtener la línea de retorno
            retorno = linea.strip().split('return ')[-1].strip().rstrip(';')
            if funcion_con_parametros:
                if funcion_con_parametros['return'] is None:
                    funcion_con_parametros['return'] = ""
                funcion_con_parametros['return'] += retorno

        # Si las llaves llegan a 0, salimos de la clase
        if llaves_abiertas == 0:
            clase_actual = None

    # --- Formatear la salida en el formato requerido
    clases_info = {clase: [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones]
                   for clase, funciones in clases_y_funciones.items()}
    funciones_info = [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones_globales]

    return  clases_info, funciones_info


# ---------------------------------------------------------------------------------------------------------- TESTING
codigo_csharp = """
public class Test {
    public int Add(int a, int b) {
        return a + b;
    }

    public void PrintHello() {
        Console.WriteLine("Hello World");
        return;  // No tiene valor de retorno
    }
}

public class AnotherClass {
    public string GetName() {
        return "MyName";
    }

    private void Log(string message) {
        if(a = 1){ return false}
        else(){return True}
        Console.WriteLine(message);
    }
}

// Esta es una función global
public int Multiply(int x, int y) {
    return x * y;
}
"""  # Código C# que deseas analizar

# Llamamos a la función y obtenemos los resultados
resultado = extraer_clases_y_funciones(codigo_csharp)

# Mostramos los resultados
print(resultado)
