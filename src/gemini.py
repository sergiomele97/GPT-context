import os

import google.generativeai as genai
import pyperclip
from colorama import Fore

import secrets
import summarize


def send(prompt):
    try:
        print("Calling Gemini... \nPrompt: " + prompt)
        api_key = secrets.get_api_key()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        # Print OK result
        print(response.text)
        pyperclip.copy(response.text)
        print(
            f"{Fore.GREEN}=================================================> Summary copied to clipboard \u2705")
        return response.text

    except Exception as e:
        print(f"We encountered an error while trying to use your API key: {e}")
        print("\n Use 'context config' to configure your API key.")



# -----------------------------------------------------------
# Testing
# -----------------------------------------------------------
if __name__ == "__main__":
    send("Please generate an easy-to-read summary of the project for a person based on this information:" + summarize.generate_project_context(os.getcwd()))
