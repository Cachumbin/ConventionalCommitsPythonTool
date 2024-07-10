import tkinter as tk
from tkinter import ttk
import json

def downloadScopes()->list:
    file = open('projects.json', 'r')
    data = json.load(file)
    file.close()

    return data

def saveProjectsToFile(projects):
    with open('projects.json', 'w') as f:
        json.dump(projects, f, indent=4)


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
    if(scope.instate(['selected'])):
        scope.invoke()
    commitBreakingChange = "!" if breakingChange.instate(['selected']) else ""
    if(breakingChange.instate(['selected'])):
        breakingChange.invoke()
    commitMessage = message.get()
    commitBody = f"-m \"{bodyText.get()}\"" if body.instate(['selected']) else ""
    if(body.instate(['selected'])):
        body.invoke()
    commitFooter = f"-m \"BREAKING CHANGE: {breakingChangeFooterText.get()}\"" if breakingChangeFooter.instate(['selected']) else ""
    if(breakingChangeFooter.instate(['selected'])):
        breakingChangeFooter.invoke()

    commit = f"git commit -m \"{commitType}{commitScope}{commitBreakingChange}: {commitMessage}\" {commitBody} {commitFooter}"

    textToCopy.config(text=commit)

    root.clipboard_clear()
    root.clipboard_append(commit)

    type.set('')
    scopeBox.set('')
    message.delete(0, tk.END)
    bodyText.delete(0, tk.END)
    breakingChangeFooterText.delete(0, tk.END)

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

root = tk.Tk()
root.title("Conventional Commits Tool")
root.geometry('720x600')
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')

style.configure('TFrame', background='#505159', padding=10, margin=5)
style.configure('TButton', background='#1B3282', foreground='white', font=('Montserrat', 12, 'bold'), borderwidth=0, padding=5, margin=5)
style.configure('TLabel', background='#505159', font=('Montserrat', 12), foreground='#ffffff', padding=5, justify=tk.LEFT, margin=5)

style.configure('TEntry', background='#505159', foreground='#ffffff', font=('Montserrat', 12), fieldbackground='#505159', selectbackground='#505159', selectforeground='#ffffff', bordercolor='#ffffff', borderwidth=2, padding=5, margin=5)
style.map('TEntry',
          fieldbackground=[('disabled', '#323338')],
          foreground=[('disabled', '#ffffff')],
          selectbackground=[('disabled', '#323338')],
          selectforeground=[('disabled', '#ffffff')],
          highlightbackground=[('hover', '#0F87CB')],
          highlightcolor=[('hover', '#0F87CB')],
          borderwidth=[('disabled', 2)])

style.configure('TCheckbutton', background='#505159', foreground='#ffffff', padding=5, margin=5)
style.map('TCheckbutton',
          background=[('active', '#0F87CB')],
          foreground=[('disabled', '#a8a8a8')],
          highlightbackground=[('hover', '#0F87CB')],
          highlightcolor=[('hover', '#0F87CB')],
          fieldbackground=[('disabled', '#323338')],
          selectcolor=[('disabled', '#a8a8a8')],
          textcolor=[('disabled', '#a8a8a8')])

style.configure('Custom.TCombobox', 
                background='#505159', 
                foreground='#ffffff', 
                fieldbackground='#505159', 
                selectbackground='#505159', 
                selectforeground='#ffffff', 
                padding=5, 
                borderwidth=2,
                bordercolor='#ffffff')
style.map('Custom.TCombobox', 
          fieldbackground=[('readonly', '#505159')],
          background=[('readonly', '#505159')],
          foreground=[('readonly', '#ffffff')],
          selectbackground=[('readonly', '#505159')],
          selectforeground=[('readonly', '#ffffff')],
          highlightbackground=[('hover', '#0F87CB')],
          highlightcolor=[('hover', '#0F87CB')],
          borderwidth=[('readonly', 2)])

style.map('TButton', background=[('active', '#0F87CB')])

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

frm = ttk.Frame(root, padding=10, style='TFrame')
frm.grid(sticky='nsew')

ttk.Button(frm, text="Commit", command=show_commit_frame, style='TButton').grid(column=1, row=0, sticky='w', padx=5, pady=5)
ttk.Button(frm, text="Projects", command=show_project_frame, style='TButton').grid(column=2, row=0, sticky='w', padx=5, pady=5)

ttk.Label(frm, text="Type", style='TLabel').grid(column=1, row=2, sticky='w', padx=5, pady=5)
breakingChange = ttk.Checkbutton(frm, text="Breaking Change", command=enableBreakingChange, style='TCheckbutton')
breakingChange.grid(column=2, row=3, sticky='w', padx=5, pady=5)
breakingChange.invoke()
breakingChange.invoke()
type = ttk.Combobox(frm, state="readonly", values=["build", "chore", "ci", "docs", "feat", "fix", "perf", "refactor", "revert", "style", "test"], style='Custom.TCombobox')
type.grid(column=1, row=3, sticky='w', padx=5, pady=5)

scope = ttk.Checkbutton(frm, text="Scope", command=enableScope, style='TCheckbutton')
scope.grid(column=1, row=6, sticky='w', padx=5, pady=5)
scope.invoke()
scope.invoke()
scopeBox = ttk.Combobox(frm, state="readonly", values=[], style='Custom.TCombobox')
scopeBox.grid(column=2, row=6, sticky='w', padx=5, pady=5)

ttk.Label(frm, text="Message", style='TLabel').grid(column=1, row=7, sticky='w', padx=5, pady=5)
message = ttk.Entry(frm, style='TEntry')
message.grid(column=1, row=8, sticky='w', padx=5, pady=5)

body = ttk.Checkbutton(frm, text="Body", command=enableBody, style='TCheckbutton')
body.grid(column=1, row=10, sticky='w', padx=5, pady=5)
body.invoke()
body.invoke()
bodyText = ttk.Entry(frm, style='TEntry')
bodyText.grid(column=2, row=10, sticky='w', padx=5, pady=5)

breakingChangeFooter = ttk.Checkbutton(frm, text="Breaking Change Footer", command=enableBreakingChangeFooter, style='TCheckbutton')
breakingChangeFooter.grid(column=1, row=12, sticky='w', padx=5, pady=5)
breakingChangeFooter.invoke()
breakingChangeFooter.invoke()
breakingChangeFooterText = ttk.Entry(frm, style='TEntry')
breakingChangeFooterText.grid(column=2, row=12, sticky='w', padx=5, pady=5)

ttk.Label(frm, text="Project Template", style='TLabel').grid(column=1, row=1, sticky='w', padx=5, pady=5)
project = ttk.Combobox(frm, state="readonly", values=names, style='Custom.TCombobox')
project.grid(column=2, row=1, sticky='w', padx=5, pady=5)

generateCommit = ttk.Button(frm, text="Generate Commit Message", command=createCommitMessage, style='TButton')
generateCommit.grid(column=3, row=13, sticky='w', padx=5, pady=5)

textToCopy = ttk.Label(frm, text='', style='TLabel', wraplength=680)
textToCopy.grid(column=1, row=14, columnspan=3, padx=5, pady=5, sticky='w')

breakingChangeFooterText.config(state='disabled')
bodyText.config(state='disabled')
scopeBox.config(state='disabled')
breakingChangeFooter.config(state='disabled')
breakingChangeFooterText.config(state='disabled')
project.bind("<<ComboboxSelected>>", update_combobox)

frm2 = ttk.Frame(root, padding=10, style='TFrame')

ttk.Button(frm2, text="Commit", command=show_commit_frame, style='TButton').grid(column=1, row=0, sticky='w', padx=5, pady=5)
ttk.Button(frm2, text="Projects", command=show_project_frame, style='TButton').grid(column=2, row=0, sticky='w', padx=5, pady=5)

ttk.Label(frm2, text="Project Template", style='TLabel').grid(column=1, row=1, sticky='w', padx=5, pady=5)
projectSelect = ttk.Combobox(frm2, state="readonly", values=names, style='Custom.TCombobox')
projectSelect.grid(column=2, row=1, sticky='w', padx=5, pady=5)

ttk.Label(frm2, text="Scopes", style='TLabel').grid(column=1, row=2, sticky='w', padx=5, pady=5)
scopeBox2 = ttk.Combobox(frm2, state="readonly", values=[], style='Custom.TCombobox')
scopeBox2.grid(column=2, row=2, sticky='w', padx=5, pady=5)
newProject = ttk.Entry(frm2, style='TEntry')
newProject.grid(column=3, row=1, sticky='w', padx=5, pady=5)

generateProject = ttk.Button(frm2, text="Create Project Template", command=createProject, style='TButton')
generateProject.grid(column=4, row=1, sticky='w', padx=5, pady=5)

projectSelect.bind("<<ComboboxSelected>>", update_combobox2)

ttk.Label(frm2, text="Add Scopes", style='TLabel').grid(column=1, row=3, sticky='w', padx=5, pady=5)

newScope = ttk.Entry(frm2, style='TEntry')
newScope.grid(column=1, row=4, sticky='w', padx=5, pady=5)

generateScope = ttk.Button(frm2, text="Add Scope", command=createScope, style='TButton')
generateScope.grid(column=2, row=4, sticky='w', padx=5, pady=5)

ttk.Label(frm2, text="Delete Scopes", style='TLabel').grid(column=1, row=5, sticky='w', padx=5, pady=5)

scopeBox3 = ttk.Combobox(frm2, state="readonly", values=[], style='Custom.TCombobox')
scopeBox3.grid(column=1, row=6, sticky='w', padx=5, pady=5)

deleteScope = ttk.Button(frm2, text="Delete Scope", command=deleteScope, style='TButton')
deleteScope.grid(column=2, row=6, sticky='w', padx=5, pady=5)

projectSelect.bind("<<ComboboxSelected>>", update_combobox2)

root.mainloop()
