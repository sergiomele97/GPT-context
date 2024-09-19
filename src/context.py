import argparse
import api_key_config  # Asegúrate de que este módulo esté disponible
import init
import add
import context_tools


def main():

    parser = argparse.ArgumentParser(description="Context management tool.")
    subparsers = parser.add_subparsers(dest='command')

    # Command 'init'
    subparsers.add_parser('init', help='Initialize a new context repository.')

    # Command 'add'
    add_parser = subparsers.add_parser('add', help='Add a new context to the repository.')
    add_parser.add_argument('prompt', help='The prompt for the context.')

    # Command 'config' for configuring API key
    subparsers.add_parser('config', help='Configure API key.')

    args = parser.parse_args()


    if args.command == 'init':
        init.init_context_repo()
    elif args.command == 'add':
        add.add_context(args.prompt)
    elif args.command == 'config':
        api_key_config.execute()  # Call the API key config function
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
