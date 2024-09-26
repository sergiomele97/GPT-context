from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("huggingface/CodeParrot-small")
model = AutoModelForCausalLM.from_pretrained("huggingface/CodeParrot-small")

inputs = tokenizer("def suma(a, b):", return_tensors="pt")
outputs = model.generate(**inputs)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
