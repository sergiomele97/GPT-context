import argparse
import os
import summarize
import directory  # Import the function from the new file
import file  # Make sure the add() function is in file.py
import gemini

def main():
    parser = argparse.ArgumentParser(description="Context management tool.")
    parser.add_argument('command', nargs='?', help="Type 'help' or 'h' to display help.")
    parser.add_argument('args', nargs=argparse.REMAINDER, help="Additional arguments for commands.")

    args = parser.parse_args()

    if args.command is None:
        # If no command is specified
        print("Command 'context' executed. Use 'context help' or 'context h' for assistance.")
        summarize.generate_project_context(os.getcwd())

    elif args.command in ['help', 'h']:
        # If the user requests help
        print("""
        Context Command System:
        --------------------------------
        - 'context': Executes the main command.
        - 'context help' or 'context h': Displays this help information.
        - 'context init': Initializes the context.
        - 'context add <file_path>': Adds a file to the current context.
        - 'context check': Verifies and shows the files in the current context.
        - 'context ia': Generates a project summary using AI.
        """)

    elif args.command == 'init':
        directory.init(os.getcwd())  # Calls the imported function

    elif args.command == 'add':
        if len(args.args) < 1:
            print("Please provide the path of the file you want to add.")
        else:
            file.add(args.args[0])  # Calls the add function in file.py

    elif args.command == 'check':
        if len(args.args) < 1:  # context check => list current context
            print("To list all contexts: context list")
            print("To switch to a context or create a new one: context check #context_name")
            file.check()
        else:
            file.change_context(args.args[0])  # context check name => change context
            file.check()

    elif args.command == 'list':
        file.list()
    elif args.command == 'ia':
        gemini.send("Please generate an easy-to-read project summary for a person based on this information: " + summarize.generate_project_context(os.getcwd()))

    else:
        print(f"Command '{args.command}' not recognized. Use 'context help' or 'context h' for assistance.")

    input("Press Enter to close the program...")

if __name__ == "__main__":
    main()
