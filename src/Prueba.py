from transformers import RobertaTokenizer, RobertaModel, T5Tokenizer, T5ForConditionalGeneration
import os
import torch
import re

# Cargar el tokenizer y modelo de T5 para la generación de texto
t5_tokenizer = T5Tokenizer.from_pretrained('t5-small')
t5_model = T5ForConditionalGeneration.from_pretrained('t5-small')

# Función para leer archivos y obtener su contenido
def read_project_files(directory):
    project_files = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.java', '.js', '.md', '.txt')):  # Filtrar archivos relevantes
                file_path = os.path.join(root, file)
                # Abrir el archivo con codificación UTF-8
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    project_files[file_path] = f.read()
    return project_files

# Función para resumir archivos del proyecto utilizando T5
def summarize_project(project_directory):
    files_content = read_project_files(project_directory)
    summary = ""

    for file_path, content in files_content.items():
        # Tokenización del contenido para T5
        inputs = t5_tokenizer("summarize: " + content, return_tensors="pt", truncation=True, max_length=512, padding=True)

        # Obtener resúmenes generados
        with torch.no_grad():
            outputs = t5_model.generate(**inputs, max_length=150, num_beams=4, early_stopping=True)
            summary_text = t5_tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Agregar al resumen general
        summary += f"\nFile: {file_path}\n"
        summary += f"Resumen: {summary_text}\n"

    return summary

# Directorio de ejemplo del proyecto
project_directory = "C:\\Work\\3-GPT-context\\src"

# Obtener resumen del proyecto
project_summary = summarize_project(project_directory)
print(project_summary)
