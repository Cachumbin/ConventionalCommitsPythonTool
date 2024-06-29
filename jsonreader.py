import json

file = open('projects.json', 'r')

json.decoder(file)
data = json.load(file)

file.close()

print(data)
