import google.generativeai as genai
import api_key_config
import time
import json
import os
from src.comandos_viejos import directory


def send(prompt):
    try:
        print("Llamando a gemini... \nPrompt: " + prompt)
        api_key = api_key_config.load_api_key()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        time.sleep(3)
        return response.text

    except Exception as e:
        print(f"We encountered an error while trying to use your API key: {e}")
        print("\n Use 'context config' to configure your api key.")
        time.sleep(3)

def send_until_json(prompt):
    while True:
        answer = send(prompt)
        try:
            # Intentamos cargar la respuesta como JSON
            json_response = json.loads(answer)
            time.sleep(3)
            return json_response  # Si es válido, lo devolvemos
        except json.JSONDecodeError:
            # Si no es un JSON válido, esperamos 3 segundos y volvemos a intentar
            time.sleep(3)
            continue

    return answer


def choose_files(prompt):
    rules = 'Tu respuesta debe ser unicamente un JSON, no escribas nada de texto, no escribas comillas antes y despues ni escribas json. Quiero que me ayudes a añadir funcionalidades en este proyecto. Devuelveme únicamente un json con una lista con el nombre de los archivos que consideras que necesitas ver para tener la mayor información posible para responder a posteriores preguntas de como seguir desarrollando código en este proyecto. El resumen que te mando es desde un directorio raiz, ES MUY IMPORTANTE QUE todas las rutas que me devuelvas deben comenzar desde ese directorio.'
    finalprompt = prompt + rules

    return send_until_json(finalprompt)


def summarize_files(file_list):
    root_dir = os.path.dirname(os.path.dirname(directory.find_context_repo(os.getcwd())))

    if root_dir is None:
        return "No se encontró el directorio .context."

    result = []

    for file_name in file_list:
        file_path = os.path.join(root_dir, file_name)
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                result.append(f"=== {file_path} ===\n{content}\n")
        except Exception as e:
            result.append(f"Error al abrir {file_path}: {str(e)}\n")

    return ''.join(result)


