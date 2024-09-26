import re
from transformers import AutoTokenizer, AutoModelForCausalLM

# Cargar el modelo y el tokenizador
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-350M-mono")
model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-350M-mono")

# Ruta del archivo que deseas abrir
file_path = r"C:\Work\3-GPT-context\src\gemini.py"

# Abrir y leer el archivo
with open(file_path, 'r', encoding='utf-8') as file:
    code_snippet = file.read()

# Dividir el código en funciones
function_pattern = r'(def\s+[A-Za-z_][A-Za-z0-9_]*\s*\(.*?\):)'
function_definitions = re.findall(function_pattern, code_snippet)
functions = []

# Buscar las funciones en el código
for func in function_definitions:
    start_index = code_snippet.find(func)
    end_index = start_index + code_snippet[start_index:].find('\n\n')  # Encuentra el final de la función
    function_code = code_snippet[start_index:end_index]
    functions.append(function_code)

# Generar explicaciones para cada función
explanations = []
for function_code in functions:
    input_text = f"Explain the following code:\n\n{function_code}\n\nExplanation:"
    inputs = tokenizer(input_text, return_tensors='pt')

    # Generar la explicación
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        repetition_penalty=2.0,
        pad_token_id=tokenizer.eos_token_id,
    )

    explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    explanations.append(explanation)

# Combinar todas las explicaciones en un resumen
final_summary = "\n".join(explanations)

# Mostrar el resumen final
print("Final Summary of Explanations:")
print(final_summary)
