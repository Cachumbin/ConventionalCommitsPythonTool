import jsonreader
import tkinter as tk
from tkinter import ttk

projects = jsonreader.downloadScopes()
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

def createCommitMessage(*args):
    commitType = type.get()
    commitScope = f"({scopeBox.get()})" if scope.instate(['selected']) else ""
    commitBreakingChange = "!" if breakingChange.instate(['selected']) else ""
    commitMessage = message.get()
    commitBody = f"-m \"{bodyText.get()}\"" if body.instate(['selected']) else ""
    commitFooter = f"-m \"BREAKING CHANGE: {breakingChangeFooterText.get()}\"" if breakingChangeFooter.instate(['selected']) else ""

    commit = f"git commit -m \"{commitType}{commitScope}{commitBreakingChange}: {commitMessage}\" {commitBody} {commitFooter}"

    textToCopy = ttk.Label(frm, text=commit)
    textToCopy.grid(column=1, row=14, columnspan=2)

    root.clipboard_clear()
    root.clipboard_append(commit)

    type.set('')
    scopeBox.set('')
    message.delete(0, tk.END)
    bodyText.delete(0, tk.END)
    breakingChangeFooterText.delete(0, tk.END)

def show_commit_frame():
    frm2.grid_forget()
    frm.grid()

def show_project_frame():
    frm.grid_forget()
    frm2.grid()

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

        jsonreader.saveProjectsToFile(projects)

def createScope():
    newScopeName = newScope.get()
    projectAddScope = projectSelect.get()
    for i in projects:
        if projectAddScope == i["name"]:
            i["scopes"].append(newScopeName)
            update_combobox2()
            break

    newScope.delete(0, tk.END)
    jsonreader.saveProjectsToFile(projects)

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
    jsonreader.saveProjectsToFile(projects)

root = tk.Tk()
root.title("Conventional Commits Tool")
root.geometry('600x450')
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')

style.configure('TFrame', background='#f0f0f0')
style.configure('TButton', background='#4CAF50', foreground='white', font=('Helvetica', 10, 'bold'))
style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
style.configure('TEntry', background='#ffffff')
style.configure('TCombobox', background='#ffffff')

frm = ttk.Frame(root, padding=10, style='TFrame')
frm.grid()

ttk.Button(frm, text="Commit", command=show_commit_frame, style='TButton').grid(column=1, row=0)
ttk.Button(frm, text="Projects", command=show_project_frame, style='TButton').grid(column=2, row=0)

ttk.Label(frm, text="Type", style='TLabel').grid(column=1, row=2)
breakingChange = ttk.Checkbutton(frm, text="Breaking Change", command=enableBreakingChange, style='TCheckbutton')
breakingChange.grid(column=2, row=3)
breakingChange.invoke()
breakingChange.invoke()
type = ttk.Combobox(frm, state="readonly", values=["build", "chore", "ci", "docs", "feat", "fix", "perf", "refactor", "revert", "style", "test"], style='TCombobox')
type.grid(column=1, row=3)

scope = ttk.Checkbutton(frm, text="Scope", command=enableScope, style='TCheckbutton')
scope.grid(column=1, row=6)
scope.invoke()
scope.invoke()
scopeBox = ttk.Combobox(frm, state="readonly", values=[], style='TCombobox')
scopeBox.grid(column=2, row=6)

ttk.Label(frm, text="Message", style='TLabel').grid(column=1, row=7)
message = ttk.Entry(frm, style='TEntry')
message.grid(column=1, row=8)

body = ttk.Checkbutton(frm, text="Body", command=enableBody, style='TCheckbutton')
body.grid(column=1, row=10)
body.invoke()
body.invoke()
bodyText = ttk.Entry(frm, style='TEntry')
bodyText.grid(column=2, row=10)

breakingChangeFooter = ttk.Checkbutton(frm, text="Breaking Change Footer", command=enableBreakingChangeFooter, style='TCheckbutton')
breakingChangeFooter.grid(column=1, row=12)
breakingChangeFooter.invoke()
breakingChangeFooter.invoke()
breakingChangeFooterText = ttk.Entry(frm, style='TEntry')
breakingChangeFooterText.grid(column=2, row=12)

ttk.Label(frm, text="Project Template", style='TLabel').grid(column=1, row=1)
project = ttk.Combobox(frm, state="readonly", values=names, style='TCombobox')
project.grid(column=2, row=1)

generateCommit = ttk.Button(frm, text="Generate Commit Message", command=createCommitMessage, style='TButton')
generateCommit.grid(column=1, row=13)

breakingChangeFooterText.config(state='disabled')
bodyText.config(state='disabled')
scopeBox.config(state='disabled')
breakingChangeFooter.config(state='disabled')
breakingChangeFooterText.config(state='disabled')
project.bind("<<ComboboxSelected>>", update_combobox)

frm2 = ttk.Frame(root, padding=10, style='TFrame')

ttk.Button(frm2, text="Commit", command=show_commit_frame, style='TButton').grid(column=1, row=0)
ttk.Button(frm2, text="Projects", command=show_project_frame, style='TButton').grid(column=2, row=0)

ttk.Label(frm2, text="Project Template", style='TLabel').grid(column=1, row=1)
projectSelect = ttk.Combobox(frm2, state="readonly", values=names, style='TCombobox')
projectSelect.grid(column=2, row=1)

ttk.Label(frm2, text="Scopes", style='TLabel').grid(column=1, row=2)
scopeBox2 = ttk.Combobox(frm2, state="readonly", values=[], style='TCombobox')
scopeBox2.grid(column=2, row=2)
newProject = ttk.Entry(frm2, style='TEntry')
newProject.grid(column=3, row=1)

generateProject = ttk.Button(frm2, text="Create Project Template", command=createProject, style='TButton')
generateProject.grid(column=4, row=1)

projectSelect.bind("<<ComboboxSelected>>", update_combobox2)

ttk.Label(frm2, text="Add Scopes", style='TLabel').grid(column=1, row=3)

newScope = ttk.Entry(frm2, style='TEntry')
newScope.grid(column=1, row=4)

generateScope = ttk.Button(frm2, text="Add Scope", command=createScope, style='TButton')
generateScope.grid(column=2, row=4)

ttk.Label(frm2, text="Delete Scopes", style='TLabel').grid(column=1, row=5)

scopeBox3 = ttk.Combobox(frm2, state="readonly", values=[], style='TCombobox')
scopeBox3.grid(column=1, row=6)

deleteScope = ttk.Button(frm2, text="Delete Scope", command=deleteScope, style='TButton')
deleteScope.grid(column=2, row=6)

projectSelect.bind("<<ComboboxSelected>>", update_combobox2)

root.mainloop()