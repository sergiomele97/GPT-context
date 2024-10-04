import re

def extract_info(codigo_perl):
    # --------------------------------------------------------------------------------------------------- Parámetros

    # ---REGEX---------
    regex_paquetes = r'package\s+([A-Za-z_][A-Za-z0-9_]*)'
    regex_subrutinas = r'sub\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{'
    regex_return = r'return\s+([^;]+);?'  # Capturar el valor después del 'return'
    regex_imports = r'use\s+([A-Za-z_][A-Za-z0-9_:]*)'  # Capturar imports

    # ---OUTPUT--------
    paquetes_y_subrutinas = {}
    subrutinas_globales = []
    imports_info = []

    # ---VARIABLES-----
    paquete_actual = None
    llaves_abiertas = 0  # Contador de {}
    subrutina_con_parametros = None  # Inicializar aquí para evitar el error

    # ------------------------------------------------------------------------------------------ Lectura linea a linea
    lineas = codigo_perl.splitlines()

    for linea in lineas:
        llaves_abiertas += linea.count('{') - linea.count('}')

        # ----------------------------------- Buscar imports
        importacion = re.search(regex_imports, linea)
        if importacion:
            imports_info.append(importacion.group(1).strip())
            continue

        # ----------------------------------- Buscar paquetes (similar a clases)
        paquete = re.search(regex_paquetes, linea)
        if paquete:
            paquete_actual = paquete.group(1)
            paquetes_y_subrutinas[paquete_actual] = []  # Inicializar la lista de subrutinas para este paquete
            llaves_abiertas = 1
            continue

        # ------------------------------------ Buscar subrutinas (funciones)
        subrutina = re.search(regex_subrutinas, linea)
        if subrutina:
            nombre_subrutina = subrutina.group(1)
            subrutina_con_parametros = {'name': nombre_subrutina, 'return': ''}

            if paquete_actual and llaves_abiertas > 0:
                # Si estamos dentro de un paquete, agregamos la subrutina a ese paquete
                paquetes_y_subrutinas[paquete_actual].append(subrutina_con_parametros)
            else:
                # Si no estamos dentro de un paquete, es una subrutina global
                subrutinas_globales.append(subrutina_con_parametros)

        # ------------------------------------ Buscar return usando regex
        retorno = re.search(regex_return, linea)
        if retorno and subrutina_con_parametros:  # Verificar que subrutina_con_parametros está inicializada
            valor_retorno = retorno.group(1).strip()
            if subrutina_con_parametros['return']:
                subrutina_con_parametros['return'] += f"; {valor_retorno}"  # Añadir con separación
            else:
                subrutina_con_parametros['return'] = valor_retorno  # Almacenar solo el valor de retorno

        # Si las llaves llegan a 0, salimos del paquete
        if llaves_abiertas == 0:
            paquete_actual = None

    # --- Formatear la salida en el formato requerido
    paquetes_info = {paquete: [{'name': f['name'], 'return': f['return']} for f in subrutinas]
                     for paquete, subrutinas in paquetes_y_subrutinas.items()}
    subrutinas_info = [{'name': f['name'], 'return': f['return']} for f in subrutinas_globales]

    return imports_info, paquetes_info, subrutinas_info


# ---------------------------------------------------------------------------------------------------------- TESTING
if __name__ == "__main__":
    # Código Perl de ejemplo
    codigo_perl = """
    use strict;
    use warnings;

    package Test;

    sub add {
        my ($a, $b) = @_;
        return $a + $b;
    }

    sub print_hello {
        print "Hello World\n";
        return;
    }

    package AnotherClass;

    sub get_name {
        return "MyName";
    }

    sub log {
        my ($message) = @_;
        if ($a == 1) { return 0; }
        else { return 1; }
        print $message;
    }

    # Esta es una subrutina global
    sub multiply {
        my ($x, $y) = @_;
        return $x * $y;
    }
    """  # Código Perl que deseas analizar

    # Llamamos a la función y obtenemos los resultados
    imports_info, paquetes_info, subrutinas_info = extract_info(codigo_perl)

    # Mostramos los resultados
    print("Imports encontrados:")
    print(imports_info)
    print("Paquetes y subrutinas encontradas:")
    print(paquetes_info)
    print("Subrutinas globales encontradas:")
    print(subrutinas_info)

    # Definir la salida esperada
    salida_esperada_imports = ['strict', 'warnings']
    salida_esperada_paquetes = {
        'Test': [
            {'name': 'add', 'return': '$a + $b'},
            {'name': 'print_hello', 'return': ''}
        ],
        'AnotherClass': [
            {'name': 'get_name', 'return': '"MyName"'},
            {'name': 'log', 'return': '0; 1'}
        ]
    }

    salida_esperada_globales = [
        {'name': 'multiply', 'return': '$x * $y'}
    ]

    # Comprobamos que los resultados coincidan con la salida esperada
    if imports_info == salida_esperada_imports and paquetes_info == salida_esperada_paquetes and subrutinas_info == salida_esperada_globales:
        print("Prueba exitosa: Los resultados son los esperados.")
    else:
        print("Prueba fallida: Los resultados no coinciden con lo esperado.")
