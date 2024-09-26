import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Cargar el tokenizador y el modelo
model_name = "meta-llama/Llama-3.1-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Si tienes GPU, puedes mover el modelo a la GPU
if torch.cuda.is_available():
    model = model.to('cuda')


# Función para generar texto
def generate_text(prompt, max_length=50):
    inputs = tokenizer(prompt, return_tensors="pt")

    # Mover los tensores a la GPU si está disponible
    if torch.cuda.is_available():
        inputs = {k: v.to('cuda') for k, v in inputs.items()}

    outputs = model.generate(**inputs, max_length=max_length, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# Ejemplo de uso
prompt = "¿Cuáles son los beneficios de la inteligencia artificial?"
generated_text = generate_text(prompt)
print(generated_text)
