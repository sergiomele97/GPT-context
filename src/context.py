import argparse
import os

import summarize


def main():

    parser = argparse.ArgumentParser(description="Context management tool.")
    parser.add_argument('command', nargs='?', help="Type 'help' or 'h' to display help.")

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
        """)
    else:
        print(f"Comando '{args.command}' no reconocido. Usa 'context help' o 'context h' para obtener ayuda.")

if __name__ == "__main__":
    main()