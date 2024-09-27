import re

def extraer_clases_y_funciones(codigo_csharp):
    # Expresión regular para encontrar clases
    global funcion_con_parametros
    regex_clases = r'class\s+([A-Za-z_][A-Za-z0-9_]*)'

    # Expresión regular para encontrar funciones/métodos con parámetros
    regex_funciones = r'(public|private|protected|internal)\s+[A-Za-z_][A-Za-z0-9_<>]*\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)'

    # Diccionario para almacenar las clases y sus funciones
    clases_y_funciones = {}

    # Lista para almacenar funciones globales
    funciones_globales = []

    # Variables de control para identificar si estamos dentro de una clase
    clase_actual = None
    llaves_abiertas = 0  # Contador de llaves '{' y '}'

    # Identificar si estamos dentro de una funcion
    function_opened = False

    # Procesamos el código para encontrar clases y funciones
    lineas = codigo_csharp.splitlines()

    for linea in lineas:
        # Actualizamos el contador de llaves
        llaves_abiertas += linea.count('{') - linea.count('}')

        # Buscar clases
        clase = re.search(regex_clases, linea)
        if clase:
            clase_actual = clase.group(1)
            clases_y_funciones[clase_actual] = []  # Inicializar la lista de funciones para esta clase
            llaves_abiertas = 1  # Cuando abrimos una clase, empezamos con una llave abierta
            continue  # Pasamos a la siguiente línea, no puede haber funciones en la misma línea que la clase

        # Buscar funciones
        funcion = re.search(regex_funciones, linea)
        if funcion:

            nombre_funcion = funcion.group(2)
            parametros = funcion.group(3).split(',') if funcion.group(3).strip() else []
            parametros = [param.strip() for param in parametros]  # Limpiar espacios
            funcion_con_parametros = {'name': nombre_funcion, 'params': parametros, 'return': "None"}
            function_opened = True

            if clase_actual and llaves_abiertas > 0:
                # Si estamos dentro de una clase, agregamos la función a esa clase
                funcion_con_parametros['return'] = None  # Inicializar retorno
                clases_y_funciones[clase_actual].append(funcion_con_parametros)
            else:
                # Si no estamos dentro de una clase, es una función global
                funcion_con_parametros['return'] = None  # Inicializar retorno
                funciones_globales.append(funcion_con_parametros)

        # Detectar return dentro de funciones
        if 'return ' in linea and function_opened == True:
            # Obtener la línea de retorno
            retorno = linea.strip().split('return ')[-1].strip().rstrip(';')
            if funcion_con_parametros:
                if funcion_con_parametros['return'] is None:
                    funcion_con_parametros['return'] = ""
                funcion_con_parametros['return'] += retorno

        # Si las llaves llegan a 0, salimos de la clase
        if llaves_abiertas == 0:
            clase_actual = None

    # Formatear la salida en el formato requerido
    clases_info = {clase: [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones]
                   for clase, funciones in clases_y_funciones.items()}
    funciones_info = [{'name': f['name'], 'params': f['params'], 'return': f['return']} for f in funciones_globales]

    return  clases_info, funciones_info

# Ejemplo de uso
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
