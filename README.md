# GPT-Context Installer

This is a tool designed to optimize and standardize interaction with CHATGPT and other AIs.

## Installation

1. **Double-click** on the executable called `GPT-context-installer` located in the root directory.
   
2. Once the installation is complete, **open your terminal** and type `context`.

3. If you receive a message explaining the available commands, the installation was successful!

---

## Additional Information

You can ignore the rest of this document if you only need to install and use GPT-context. Below is a more detailed explanation of what the installer does:

- The installer is a C# console application created with Visual Studio. **Important:** It has only been tested on Windows.

- The installer will:
  - Create a virtual environment in your Documents folder.
  - Activate the virtual environment, then install `pip` and `pyinstaller` using `pip`.

  *(Note: You can delete the virtual environment from your Documents folder once the installation is complete.)*

  - Create a new folder called `GPT-context` in your Program Files folder. This is where the application will be installed.

  - Add the `GPT-context` folder to the PATH environment variable, so you can use the `context` command from any terminal.
