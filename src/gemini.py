import os

import google.generativeai as genai
import secrets
from src import summarize


def send(prompt):
    try:
        print("Llamando a gemini... \nPrompt: " + prompt)
        api_key = secrets.get_api_key()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        print(response.text)
        return response.text

    except Exception as e:
        print(f"We encountered an error while trying to use your API key: {e}")
        print("\n Use 'context config' to configure your api key.")



# -----------------------------------------------------------
# Testing
# -----------------------------------------------------------
if __name__ == "__main__":
    send("Por favor, generame un resumen del proyecto facil de leer para una persona a partir de esta informacion:" + summarize.generate_project_context(os.getcwd()))
