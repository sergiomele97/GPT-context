import re

def extract_functions_and_classes(codigo_csharp):

    # --------------------------------------------------------------------------------------------------- Parámetros

    global funcion_con_parametros

    # ---REGEX---------
    regex_clases = r'class\s+([A-Za-z_][A-Za-z0-9_]*)'
    regex_funciones = r'(public|private|protected|internal)\s+[A-Za-z_][A-Za-z0-9_<>]*\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)'
    regex_return = r'return\s+([^;]+);?'  # Capturar el valor después del 'return'

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

        # ------------------------------------ Buscar return usando regex
        retorno = re.search(regex_return, linea)
        if retorno:
            valor_retorno = retorno.group(1).strip()
            if funcion_con_parametros:
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

    return  clases_info, funciones_info


# ---------------------------------------------------------------------------------------------------------- TESTING
if __name__ == "__main__":
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
    clases_info, funciones_info  = extract_functions_and_classes(codigo_csharp)

    # Mostramos los resultados
    print(clases_info)
    print(funciones_info)
