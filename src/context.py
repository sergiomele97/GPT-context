import argparse
import os
import summarize
import directory  # Importa la función desde el nuevo archivo

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
        - 'context add <nombre> <archivos...>': Agrega un contexto personalizado (disponible en futuras versiones).
        """)

    elif args.command == 'init':
        directory.init()  # Llama a la función importada

    elif args.command == 'add':
        print("Comando 'add' reconocido. La funcionalidad estará disponible en futuras versiones.")

    else:
        print(f"Comando '{args.command}' no reconocido. Usa 'context help' o 'context h' para obtener ayuda.")

    input("Presiona Enter para cerrar el programa...")

if __name__ == "__main__":
    main()
