import os
import getpass

from colorama import Fore
from cryptography.fernet import Fernet
import base64
import hashlib


def configure_api_key():
    # Prompt the user to enter the API key
    api_key = input("Enter your API key: ")

    # Generate the key from the username
    key = generate_key()

    # Encrypt the API key with the key
    encrypted_api_key = encrypt_api_key(api_key, key)

    # Save the encrypted API key in the file
    save_encrypted_api_key(encrypted_api_key)

def get_api_key():
    # Generate the key from the username
    key = generate_key()

    # Load the encrypted API key
    loaded_encrypted_key = load_encrypted_api_key()

    # Decrypt the API key
    decrypted_api_key = decrypt_api_key(loaded_encrypted_key, key)

    print(f"API key retrieved")
    return decrypted_api_key

def generate_key():
    """Generates a key from the username."""
    # Get the username
    username = getpass.getuser()
    # Hash the username using SHA256
    sha256_hash = hashlib.sha256(username.encode()).digest()
    # Take the first 32 bytes and convert them to base64
    key = base64.urlsafe_b64encode(sha256_hash[:32])
    return key


def encrypt_api_key(api_key, key):
    """Encrypts the API key using the generated key."""
    fernet = Fernet(key)
    encrypted = fernet.encrypt(api_key.encode())
    return encrypted


def save_encrypted_api_key(encrypted_key):
    """Saves the encrypted API key in a file."""
    username = getpass.getuser()
    directory = f"C:\\Users\\{username}\\AppData\\Local\\GPT-context"

    # Create the directory if it does not exist
    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, "config.txt")

    with open(file_path, 'wb') as file:
        file.write(encrypted_key)

    print(f"{Fore.GREEN}API key configured.")


def load_encrypted_api_key():
    """Loads the encrypted API key from the file."""
    username = getpass.getuser()
    file_path = f"C:\\Users\\{username}\\AppData\\Local\\GPT-context\\config.txt"

    with open(file_path, 'rb') as file:
        encrypted_key = file.read()

    return encrypted_key


def decrypt_api_key(encrypted_key, key):
    """Decrypts the API key using the generated key."""
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_key).decode()
    return decrypted


if __name__ == "__main__":
    configure_api_key()
    get_api_key()
