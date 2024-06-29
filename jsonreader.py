import json

def downloadScopes()->list:
    file = open('projects.json', 'r')
    data = json.load(file)
    file.close()

    return data
