import google.generativeai as genai
import api_key_config
import json
import os
import context_tools


def ask(prompt):
    try:
        api_key = api_key_config.load_api_key()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        print(response.text)

    except Exception as e:
        print(f"We encountered an error while trying to use your API key: {e}")
        print("\n Use 'context config' to configure your api key.")

def summarize(prompt):

    rules ="En el JSON tienes un prompt a una IA, dime que archivos de este proyecto necesitarias ver para responderlo"

    ask(rules + json.dumps(prompt))