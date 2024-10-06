import os
import getpass

from colorama import Fore
from cryptography.fernet import Fernet
import base64
import hashlib


def configurar_api_key():
    # Solicitar al usuario que introduzca la API key
    api_key = input("Introduce tu API key: ")

    # Generar la clave a partir del nombre de usuario
    key = generate_key()

    # Encriptar la API key con la clave
    encrypted_api_key = encrypt_api_key(api_key, key)

    # Guardar la API key encriptada en el archivo
    save_encrypted_api_key(encrypted_api_key)

def get_api_key():
    # Generar la clave a partir del nombre de usuario
    key = generate_key()

    # Cargar la API key encriptada
    loaded_encrypted_key = load_encrypted_api_key()

    # Desencriptar la API key
    decrypted_api_key = decrypt_api_key(loaded_encrypted_key, key)

    print(f"API key recuperada")
    return decrypted_api_key

def generate_key():
    """Genera una clave a partir del nombre de usuario."""
    # Obtener el nombre de usuario
    username = getpass.getuser()
    # Hashear el nombre de usuario usando SHA256
    sha256_hash = hashlib.sha256(username.encode()).digest()
    # Tomar los primeros 32 bytes y convertirlos a base64
    key = base64.urlsafe_b64encode(sha256_hash[:32])
    return key


def encrypt_api_key(api_key, key):
    """Encripta la API key usando la clave generada."""
    fernet = Fernet(key)
    encrypted = fernet.encrypt(api_key.encode())
    return encrypted


def save_encrypted_api_key(encrypted_key):
    """Guarda la API key encriptada en un archivo."""
    username = getpass.getuser()
    directory = f"C:\\Users\\{username}\\AppData\\Local\\GPT-context"

    # Crear el directorio si no existe
    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, "config.txt")

    with open(file_path, 'wb') as file:
        file.write(encrypted_key)

    print(f"{Fore.GREEN}API key configurada.")


def load_encrypted_api_key():
    """Carga la API key encriptada desde el archivo."""
    username = getpass.getuser()
    file_path = f"C:\\Users\\{username}\\AppData\\Local\\GPT-context\\config.txt"

    with open(file_path, 'rb') as file:
        encrypted_key = file.read()

    return encrypted_key


def decrypt_api_key(encrypted_key, key):
    """Desencripta la API key usando la clave generada."""
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_key).decode()
    return decrypted


if __name__ == "__main__":
    configurar_api_key()
    get_api_key()
