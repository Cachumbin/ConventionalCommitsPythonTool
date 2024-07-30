#modules
import tkinter as tk
from tkinter import ttk, filedialog
import json
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import subprocess

# Global variable to store the selected repository path
repo_path = ""

# functions
def downloadScopes() -> list:
    with open('projects.json', 'r') as file:
        data = json.load(file)
    return data

def saveProjectsToFile(projects):
    with open('projects.json', 'w') as f:
        json.dump(projects, f, indent=4)
    updateProjects()

def updateProjects():
    projects = downloadScopes()
    names = [project["name"] for project in projects]
    project["values"] = names

projects = downloadScopes()
names = [project["name"] for project in projects]

def update_combobox(*args):
    selected_value = project.get()
    for i in projects:
        if selected_value == i["name"]:
            scopeBox["values"] = i["scopes"]
            scopeBox.current(0)
            break

def update_combobox2(*args):
    selected_value = projectSelect.get()
    scopeBox2["values"] = []
    scopeBox3["values"] = []
    for i in projects:
        if selected_value == i["name"]:
            scopeBox2["values"] = i["scopes"]
            scopeBox2.current(0)
            scopeBox3["values"] = i["scopes"]
            scopeBox3.current(0)
            break

def enableBreakingChange():
    if breakingChange.instate(['selected']):
        breakingChangeFooter.config(state='normal')
        if breakingChangeFooter.instate(["selected"]):
            breakingChangeFooterText.config(state='normal')
        else:
            breakingChangeFooterText.config(state='disabled')
    else:
        breakingChangeFooter.config(state='disabled')
        breakingChangeFooterText.config(state='disabled')

def enableScope():
    if scope.instate(["selected"]):
        scopeBox.config(state='normal')
    else:
        scopeBox.config(state='disabled')

def enableBody():
    if body.instate(["selected"]):
        bodyText.config(state='normal')
    else:
        bodyText.config(state='disabled')

def enableBreakingChangeFooter():
    if breakingChangeFooter.instate(["selected"]):
        breakingChangeFooterText.config(state='normal')
    else:
        breakingChangeFooterText.config(state='disabled')

def changeDirectory():
    global repo_path
    try:
        subprocess.run(f"cd {repo_path}", shell=True, check=True)
        commitStatusLabel.config(text=f"Changed Directory to: {repo_path}", bootstyle="success")
    except subprocess.CalledProcessError as e:
        commitStatusLabel.config(text=f"Not changed directory to: {repo_path}", bootstyle="danger")

def createCommitMessage(*args):
    global repo_path
    commitType = type.get()
    commitScope = f"({scopeBox.get()})" if scope.instate(['selected']) else ""
    if scope.instate(['selected']):
        scope.invoke()
    commitBreakingChange = "!" if breakingChange.instate(['selected']) else ""
    if breakingChange.instate(['selected']):
        breakingChange.invoke()
    commitMessage = message.get()
    commitBody = f"-m \"{bodyText.get()}\"" if body.instate(['selected']) else ""
    if body.instate(['selected']):
        body.invoke()
    commitFooter = f"-m \"BREAKING CHANGE: {breakingChangeFooterText.get()}\"" if breakingChangeFooter.instate(['selected']) else ""
    if breakingChangeFooter.instate(['selected']):
        breakingChangeFooter.invoke()

    commit = f"git commit -m \"{commitType}{commitScope}{commitBreakingChange}: {commitMessage}\" {commitBody} {commitFooter}"

    # Run the git commit command in the selected repository path
    try:
        subprocess.run(commit, shell=True, check=True)
        commitStatusLabel.config(text="Commit successfully created!", foreground="green")
    except subprocess.CalledProcessError as e:
        commitStatusLabel.config(text=f"Error: {e}", foreground="red")

    root.clipboard_clear()
    root.clipboard_append(commit)

    type.set('')
    scopeBox.set('')
    message.delete(0, tk.END)
    bodyText.set('')
    breakingChangeFooterText.set('')

def selectRepoPath():
    global repo_path
    repo_path = filedialog.askdirectory()
    repoPathLabel.config(text=f"Selected Repo Path: {repo_path}")

def show_commit_frame():
    frm2.grid_forget()
    frm.grid(sticky='nsew')

def show_project_frame():
    frm.grid_forget()
    frm2.grid(sticky='nsew')

def createProject():
    newProjectName = newProject.get()
    if newProjectName:
        newProjectDict = {
            "name": newProjectName,
            "scopes": []
        }
        projects.append(newProjectDict)
        names.append(newProjectName)
        projectSelect["values"] = names
        project["values"] = names
        newProject.delete(0, tk.END)
        projectSelect.current(len(names) - 1)
        update_combobox2()
        saveProjectsToFile(projects)

def createScope():
    newScopeName = newScope.get()
    projectAddScope = projectSelect.get()
    for i in projects:
        if projectAddScope == i["name"]:
            i["scopes"].append(newScopeName)
            update_combobox2()
            break

    newScope.delete(0, tk.END)
    saveProjectsToFile(projects)

def deleteScope():
    scopeToDelete = scopeBox3.get()
    selectedProject = projectSelect.get()

    for project in projects:
        if project["name"] == selectedProject:
            if scopeToDelete in project["scopes"]:
                project["scopes"].remove(scopeToDelete)
                update_combobox2()
                break

    scopeBox3.set('')
    saveProjectsToFile(projects)

def editProjectName():
    selected_project_name = projectSelect.get()
    new_project_name = newProject.get()

    if selected_project_name and new_project_name:
        for project in projects:
            if project["name"] == selected_project_name:
                project["name"] = new_project_name
                break

        saveProjectsToFile(projects)
        newProject.delete(0, tk.END)
        names[names.index(selected_project_name)] = new_project_name
        projectSelect["values"] = names
        projectSelect.set(new_project_name)
        project.set(new_project_name)
        update_combobox2()

# widgets
root = ttkb.Window(themename="solar")
root.title("Conventional Commits Tool")
root.geometry('720x600')
root.resizable(False, False)

frm = ttkb.Frame(root, padding=10, bootstyle="default")
frm.grid(sticky='nsew')

ttkb.Button(frm, text="Commit", command=show_commit_frame, bootstyle="primary-outline").grid(column=1, row=0, sticky='w', padx=5, pady=5)
ttkb.Button(frm, text="Projects", command=show_project_frame, bootstyle="primary-outline").grid(column=2, row=0, sticky='w', padx=5, pady=5)

ttkb.Label(frm, text="Type", bootstyle="dark", foreground="white").grid(column=1, row=2, sticky='w', padx=5, pady=5)
breakingChange = ttkb.Checkbutton(frm, text="Breaking Change", command=enableBreakingChange, bootstyle="primary-round-toggle")
breakingChange.grid(column=2, row=3, sticky='w', padx=5, pady=5)
breakingChange.invoke()
breakingChange.invoke()
type = ttkb.Combobox(frm, state="readonly", values=["build", "chore", "ci", "docs", "feat", "fix", "perf", "refactor", "revert", "style", "test"], bootstyle="dark")
type.grid(column=1, row=3, sticky='w', padx=5, pady=5)

scope = ttkb.Checkbutton(frm, text="Scope", command=enableScope, bootstyle="primary-round-toggle")
scope.grid(column=1, row=6, sticky='w', padx=5, pady=5)
scope.invoke()
scope.invoke()
scopeBox = ttkb.Combobox(frm, state="readonly", values=[], bootstyle="dark")
scopeBox.grid(column=2, row=6, sticky='w', padx=5, pady=5)

ttkb.Label(frm, text="Message", bootstyle="dark", foreground="white").grid(column=1, row=7, sticky='w', padx=5, pady=5)
message = ttkb.Entry(frm, bootstyle="default")
message.grid(column=1, row=8, sticky='w', padx=5, pady=5)

body = ttkb.Checkbutton(frm, text="Body", command=enableBody, bootstyle="primary-round-toggle")
body.grid(column=1, row=10, sticky='w', padx=5, pady=5)
body.invoke()
body.invoke()
bodyText = ttkb.Entry(frm, bootstyle="default")
bodyText.grid(column=2, row=10, sticky='w', padx=5, pady=5)

breakingChangeFooter = ttkb.Checkbutton(frm, text="Breaking Change Footer", command=enableBreakingChangeFooter, bootstyle="primary-round-toggle")
breakingChangeFooter.grid(column=1, row=12, sticky='w', padx=5, pady=5)
breakingChangeFooter.invoke()
breakingChangeFooter.invoke()
breakingChangeFooterText = ttkb.Entry(frm, bootstyle="default")
breakingChangeFooterText.grid(column=2, row=12, sticky='w', padx=5, pady=5)

ttkb.Button(frm, text="Create Commit", command=createCommitMessage, bootstyle="primary-outline").grid(column=1, row=14, sticky='w', padx=5, pady=5)
ttkb.Label(frm, text="Commit message to copy", bootstyle="dark", foreground="white").grid(column=1, row=15, sticky='w', padx=5, pady=5)
textToCopy = ttkb.Label(frm, text="", bootstyle="dark", foreground="white")
textToCopy.grid(column=2, row=14, sticky='w', padx=5, pady=5)

# Widget to select repo path
ttkb.Button(frm, text="Select Repo Path", command=selectRepoPath, bootstyle="primary-outline").grid(column=1, row=15, sticky='w', padx=5, pady=5)
repoPathLabel = ttkb.Label(frm, text="Selected Repo Path: None", bootstyle="dark", foreground="white")
repoPathLabel.grid(column=2, row=15, sticky='w', padx=5, pady=5)

# Button to change directory
ttkb.Button(frm, text="Change Directory", command=changeDirectory, bootstyle="primary-outline").grid(column=1, row=16, sticky='w', padx=5, pady=5)

# Button to create commit
ttkb.Button(frm, text="Create Commit", command=createCommitMessage, bootstyle="success-outline").grid(column=2, row=16, sticky='w', padx=5, pady=5)

# Label to show commit status
commitStatusLabel = ttkb.Label(frm, text="", bootstyle="dark", foreground="white")
commitStatusLabel.grid(column=2, row=17, sticky='w', padx=5, pady=5)

breakingChangeFooterText.config(state='disabled')
breakingChangeFooterText.configure(bootstyle='disabled')
bodyText.config(state='disabled')
bodyText.configure(bootstyle='disabled')
scopeBox.config(state='disabled')
breakingChangeFooter.config(state='disabled')
breakingChangeFooterText.config(state='disabled')
project = ttkb.Combobox(frm, state="readonly", values=names, bootstyle="dark")
project.grid(column=2, row=1, sticky='w', padx=5, pady=5)
ttkb.Label(frm, text="Project Template", bootstyle="dark", foreground="white").grid(column=1, row=1, sticky='w', padx=5, pady=5)
project.bind("<<ComboboxSelected>>", update_combobox)

# widgets 2
frm2 = ttkb.Frame(root, padding=10, bootstyle="default")

ttkb.Button(frm2, text="Commit", command=show_commit_frame, bootstyle="primary-outline").grid(column=1, row=0, sticky='w', padx=5, pady=5)
ttkb.Button(frm2, text="Projects", command=show_project_frame, bootstyle="primary-outline").grid(column=2, row=0, sticky='w', padx=5, pady=5)

ttkb.Label(frm2, text="Project Template", bootstyle="dark", foreground="white").grid(column=1, row=1, sticky='w', padx=5, pady=5)
projectSelect = ttkb.Combobox(frm2, state="readonly", values=names, bootstyle="dark")
projectSelect.grid(column=2, row=1, sticky='w', padx=5, pady=5)

ttkb.Label(frm2, text="Scopes", bootstyle="dark", foreground="white").grid(column=1, row=2, sticky='w', padx=5, pady=5)
scopeBox2 = ttkb.Combobox(frm2, state="readonly", values=[], bootstyle="dark")
scopeBox2.grid(column=2, row=2, sticky='w', padx=5, pady=5)
newProject = ttkb.Entry(frm2, bootstyle="default")
newProject.grid(column=3, row=1, sticky='w', padx=5, pady=5)

generateProject = ttkb.Button(frm2, text="Create Project Template", command=createProject, bootstyle="primary-outline")
generateProject.grid(column=4, row=1, sticky='w', padx=5, pady=5)

editProject = ttkb.Button(frm2, text="Edit Project Name", command=editProjectName, bootstyle="primary-outline")
editProject.grid(column=4, row=2, sticky='w', padx=5, pady=5)

projectSelect.bind("<<ComboboxSelected>>", update_combobox2)

ttkb.Label(frm2, text="Add Scopes", bootstyle="dark", foreground="white").grid(column=1, row=3, sticky='w', padx=5, pady=5)

newScope = ttkb.Entry(frm2, bootstyle="default")
newScope.grid(column=1, row=4, sticky='w', padx=5, pady=5)

generateScope = ttkb.Button(frm2, text="Add Scope", command=createScope, bootstyle="primary-outline")
generateScope.grid(column=2, row=4, sticky='w', padx=5, pady=5)

ttkb.Label(frm2, text="Delete Scopes", bootstyle="dark", foreground="white").grid(column=1, row=5, sticky='w', padx=5, pady=5)

scopeBox3 = ttkb.Combobox(frm2, state="readonly", values=[], bootstyle="dark")
scopeBox3.grid(column=1, row=6, sticky='w', padx=5, pady=5)

deleteScope = ttkb.Button(frm2, text="Delete Scope", command=deleteScope, bootstyle="primary-outline")
deleteScope.grid(column=2, row=6, sticky='w', padx=5, pady=5)

projectSelect.bind("<<ComboboxSelected>>", update_combobox2)

frm.grid(sticky='nsew')

# Initialize the window
root.mainloop()
