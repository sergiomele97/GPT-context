import google.generativeai as genai
import json
import os

def execute():
  print("Running test.py")

  api_key = load_api_key()

  while True:
    try:
      genai.configure(api_key=api_key)
      model = genai.GenerativeModel("gemini-1.5-flash")
      response = model.generate_content("Write a story about a magic backpack.")
      print(response.text)

      # Api configurada con exito
      print("\n" + "*" * 40)
      print("   ✅ API Key has been configured successfully! ✅")
      print("*" * 40 + "\n")
      break  # Exit loop if API call was successful
    except Exception as e:
      print(f"We encountered an error while trying to use your API key: {e}")
      api_key = configure_api_key()

def configure_api_key():
  """Prompts the user to enter the API key and saves it to the configuration file."""
  api_key = input("Enter your API key: ")
  with open("context_config.json", "w") as f:
    json.dump({"api_key": api_key}, f)
  print("API key saved successfully.")
  return api_key

def load_api_key():
  """Loads the API key from the configuration file."""
  if os.path.exists("context_config.json"):
    try:
      with open("context_config.json", "r") as f:
        config = json.load(f)
        return config["api_key"]
    except json.JSONDecodeError:
      print("Error: The configuration file is not in a valid JSON format.")
      return None
  else:
    configure_api_key()
    return load_api_key()


if __name__ == "__main__":
  execute()