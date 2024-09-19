import google.generativeai as genai
import json
import os
import context_tools

def execute():
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
      print("WARNING: To avoid your api going public, remember to add your context_config.json to your gitignore!!!")
      print("Just add the line: **/context_config.json")
      break  # Exit loop if API call was successful
    except Exception as e:
      print(f"We encountered an error while trying to use your API key: {e}")
      api_key = configure_api_key()


def configure_api_key():
  """Prompts the user to enter the API key and saves it to the configuration file."""
  # Find the .context directory
  context_dir = context_tools.find_context_repo(os.getcwd())

  if not context_dir:
    context_tools.context_not_found(os.getcwd())
    return

  # Define the path for the configuration file
  config_file_path = os.path.join(context_dir, 'context_config.json')

  # Prompt the user for the API key
  api_key = input("Enter your API key: ")

  # Save the API key to the configuration file
  with open(config_file_path, 'w') as f:
    json.dump({"api_key": api_key}, f)

  print("API key saved successfully.")
  return api_key


def load_api_key():
  """Loads the API key from the configuration file."""
  # Find the .context directory
  context_dir = context_tools.find_context_repo(os.getcwd())

  if not context_dir:
    context_tools.context_not_found(os.getcwd())
    return

  # Define the path for the configuration file
  config_file_path = os.path.join(context_dir, 'context_config.json')

  # Check if the configuration file exists
  if os.path.exists(config_file_path):
    try:
      # Load the API key from the configuration file
      with open(config_file_path, 'r') as f:
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