import json


with open('projects.json', 'r') as file:
    data = json.load(file)


for item in data:
    print(f"Nombre: {item['project']}")
    print(f"Scopes: {', '.join(item['scopes'])}\n")