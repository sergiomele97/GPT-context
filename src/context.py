import argparse
import os
import summarize
import directory  # Importa la función desde el nuevo archivo
import file  # Asegúrate de que la función add() esté en file.py

def main():
    parser = argparse.ArgumentParser(description="Context management tool.")
    parser.add_argument('command', nargs='?', help="Type 'help' or 'h' to display help.")
    parser.add_argument('args', nargs=argparse.REMAINDER, help="Additional arguments for commands.")

    args = parser.parse_args()

    if args.command is None:
        # Si no se especifica ningún comando
        print("Comando 'context' ejecutado. Usa 'context help' o 'context h' para obtener ayuda.")
        print(summarize.generate_project_context(os.getcwd()))

    elif args.command in ['help', 'h']:
        # Si el usuario pide ayuda
        print("""
        Sistema de Comandos Context:
        --------------------------------
        - 'context': Ejecuta el comando principal.
        - 'context help' o 'context h': Muestra esta información de ayuda.
        - 'context init': Inicializa el contexto.
        - 'context add <ruta_archivo>': Agrega un archivo al contexto actual.
        - 'context check': Verifica y muestra los archivos en el contexto actual.
        - 'context ia': Genera un resumen del proyecto usando IA.
        """)

    elif args.command == 'init':
        directory.init()  # Llama a la función importada

    elif args.command == 'add':
        if len(args.args) < 1:
            print("Por favor proporciona la ruta del archivo que deseas añadir.")
        else:
            file.add(args.args[0])  # Llama a la función add en file.py

    elif args.command == 'check':
        if len(args.args) < 1: # context check => lista current context
            print("Para listar todos los contextos: context list")
            print("Para cambiar a un contexto o crear uno nuevo: context check #nombre_del_contexto")
            file.check()
        else:
            file.change_context(args.args[0])  # context check nombre => cambio de contexto
            file.check()

    elif args.command == 'ia':
        print("Comando 'context ia' ejecutado. Aquí irá la integración con IA.")

    else:
        print(f"Comando '{args.command}' no reconocido. Usa 'context help' o 'context h' para obtener ayuda.")

    input("Presiona Enter para cerrar el programa...")

if __name__ == "__main__":
    main()
