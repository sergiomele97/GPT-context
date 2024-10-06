import os

import google.generativeai as genai
from colorama import Fore

import secrets
import summarize


def send(prompt):
    try:
        print("Llamando a gemini... \nPrompt: " + prompt)
        api_key = secrets.get_api_key()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        # Imprimir resultado OK
        print(response.text)
        pyperclip.copy(response.text)
        print(
            f"{Fore.GREEN}=================================================> Summary copied to clipboard \u2705")
        return response.text

    except Exception as e:
        print(f"We encountered an error while trying to use your API key: {e}")
        print("\n Use 'context config' to configure your api key.")



# -----------------------------------------------------------
# Testing
# -----------------------------------------------------------
if __name__ == "__main__":
    send("Por favor, generame un resumen del proyecto facil de leer para una persona a partir de esta informacion:" + summarize.generate_project_context(os.getcwd()))
