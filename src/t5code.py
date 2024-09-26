import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Cargar el modelo y el tokenizer
model_name = "Salesforce/codet5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Verificar si hay una GPU disponible y usarla; de lo contrario, usar la CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

print("Versión de PyTorch:", torch.__version__)         # Verifica la versión de PyTorch
print("¿CUDA disponible?:", torch.cuda.is_available())  # Debería devolver True si la GPU está disponible

if torch.cuda.is_available():
    print("ID del dispositivo actual:", torch.cuda.current_device()) # Imprime el ID del dispositivo actual
    print("Nombre de la GPU:", torch.cuda.get_device_name(0)) # Imprime el nombre de la GPU
else:
    print("CUDA no está disponible o no se ha instalado correctamente.")

def resumir_codigo(ruta_archivo):
    # Lee el contenido del archivo
    try:
        with open(ruta_archivo, 'r') as file:
            codigo = file.read()
    except Exception as e:
        return f"Error al leer el archivo: {e}"

    # Limitar el tamaño del código a un máximo de 512 tokens
    input_text = f"Please summarize the following Python code: {codigo}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True).to(device)

    # Generar resumen
    summary_ids = model.generate(
        input_ids,
        max_length=150,
        min_length=30,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    # Decodificar el resumen
    resumen = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return resumen

# Ejemplo de uso
ruta_archivo = "C:/Work/3-GPT-context/src/gemini.py"  # Cambia esto a la ruta de tu archivo
resumen = resumir_codigo(ruta_archivo)
print("Resumen del código:\n", resumen)
