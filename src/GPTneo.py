from transformers import GPTNeoForCausalLM, GPT2Tokenizer
import torch

# Verificar si hay una GPU disponible y usarla; de lo contrario, usar CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Cargar el modelo y el tokenizador, moviendo el modelo a la GPU si está disponible
model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-2.7B").to(device)
tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-2.7B")

# Definir el texto de entrada
input_text = "¿Qué es el deep learning?"

# Tokenizar la entrada y crear la atención mask
inputs = tokenizer(input_text, return_tensors="pt").to(device)
inputs['attention_mask'] = torch.ones(inputs['input_ids'].shape, dtype=torch.long).to(device)

# Generar la salida del modelo
outputs = model.generate(
    inputs['input_ids'],
    attention_mask=inputs['attention_mask'],
    max_length=100,
    num_return_sequences=1,  # Solo devolver una secuencia
    do_sample=True,  # Permitir la variabilidad en la salida
    top_k=50,  # Mantener solo las 50 mejores probabilidades
    top_p=0.95,  # Usar muestreo acumulativo
    temperature=0.7  # Controlar la creatividad de la salida
)

# Decodificar y mostrar la salida
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
