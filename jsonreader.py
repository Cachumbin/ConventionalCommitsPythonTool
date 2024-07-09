import json

def downloadScopes()->list:
    file = open('projects.json', 'r')
    data = json.load(file)
    file.close()

    return data

def saveProjectsToFile(projects):
    with open('projects.json', 'w') as f:
        json.dump(projects, f, indent=4)
