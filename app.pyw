#modules
import tkinter as tk
from tkinter import ttk, filedialog
import json
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import subprocess
import requests
import os
import re

# Global variable to store the selected repository path
repo_path = ""
activeIssues = []

def getIssues():
    info = downloadRepoInfo()
    
    onwer = info["repo_user"]
    repo = info["repo_name"]
    
    url = f"https://api.github.com/repos/{onwer}/{repo}/issues"

    response = requests.get(url)

    if response.status_code == 200:
        issues = response.json()
        show_toast("Issues fetched successfully", 3000, True)
        return issues
    else:
        show_toast("Error getting issues", 3000, False)

# functions

def get_repo_name():
    if not repo_path or not os.path.isdir(repo_path):
        raise show_toast("Please select a valid repository path", 3000, False)
    
    bash_message = subprocess.run("git remote -v", shell=True, check=True, cwd=repo_path, stdout=subprocess.PIPE).stdout.decode('utf-8')
    repo_name = re.search(r'github\.com[:/][^/]+/([^\.]+)\.git', bash_message)
    
    if not repo_name:
        raise show_toast("No repository found in the selected path", 3000, False)
    else:
        repo_name = repo_name.group(1)
    
    repo_name_entry.delete(0, tk.END)
    repo_name_entry.insert(0, repo_name)
    
def get_repo_owner():
    if not repo_path or not os.path.isdir(repo_path):
        raise show_toast("Please select a valid repository path", 3000, False)
    
    bash_message = subprocess.run("git remote -v", shell=True, check=True, cwd=repo_path, stdout=subprocess.PIPE).stdout.decode('utf-8')
    repo_owner_str = re.search(r'git@github\.com:([^/]+)/', bash_message)
    
    if not repo_owner_str:
        raise show_toast("No owner found in the selected path", 3000, False)
    else:
        repo_owner_str = repo_owner_str.group(1)
    
    repo_user.delete(0, tk.END)
    repo_user.insert(0, repo_owner_str)
    
def downloadRepoInfo():
    with open('user_info.json', 'r') as file:
        data = json.load(file)
    return data
    
def updateRepoInfo():
    info = downloadRepoInfo()
    
    info["repo_user"] = repo_user.get()
    info["repo_name"] = repo_name_entry.get()
    
    with open('user_info.json', 'w') as f:
         json.dump(info, f, indent=4)
    show_toast("Updated the Repo information", 3000, True)
    
    
    
# def downloadScopes() -> list:
#     with open('projects.json', 'r') as file:
#         data = json.load(file)
#     return data

# def saveProjectsToFile(projects):
#     with open('projects.json', 'w') as f:
#         json.dump(projects, f, indent=4)
#     updateProjects()

# def updateProjects():
#     projects = downloadScopes()
#     names = [project["name"] for project in projects]
#     project["values"] = names

# projects = downloadScopes()
# names = [project["name"] for project in projects]

def update_combobox(*args):
    values = []
    for i in activeIssues:
        values.append(f"#{i['number']}")
    issueBox["values"] = values

# def update_combobox2(*args):
#     selected_value = projectSelect.get()
#     #scopeBox2["values"] = []
#     scopeBox3["values"] = []
#     for i in projects:
#         if selected_value == i["name"]:
#             scopeBox3["values"] = i["scopes"]
#             scopeBox3.current(0)
#             break

def enableBreakingChange():
    if breakingChange.instate(['selected']):
        breakingChangeFooter.config(state='normal')
        if breakingChangeFooter.instate(["selected"]):
            breakingChangeFooterText.config(state='normal', bootstyle='primary')
        else:
            breakingChangeFooterText.config(state='disabled')
    else:
        breakingChangeFooter.config(state='disabled')
        breakingChangeFooterText.config(state='disabled', bootstyle='dark')

def enableIssue():
    if issue.instate(["selected"]):
        issueBox.config(state='normal', bootstyle='primary')
    else:
        issueBox.config(state='disabled', bootstyle='dark')

def enableBody():
    if body.instate(["selected"]):
        bodyText.config(state='normal', bootstyle='primary')
    else:
        bodyText.config(state='disabled', bootstyle='dark')

def enableBreakingChangeFooter():
    if breakingChangeFooter.instate(["selected"]):
        breakingChangeFooterText.config(state='normal', bootstyle='primary')
    else:
        breakingChangeFooterText.config(state='disabled', bootstyle='dark')

def changeDirectory():
    global repo_path
    global activeIssues
    
    activeIssues = []
    try:
        subprocess.run(f"cd {repo_path}", shell=True, check=True)
        show_toast(f"Changed directory to: {repo_path}", 3000, True)
        issues = getIssues()
        for i in issues:
            activeIssues.append({
                "title": i["title"],
                "number": i["number"]
            })
        update_combobox()
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode('utf-8') if e.stderr else str(e)
        show_toast(f"{error_message}", 3000, False)

def createCommitMessage(*args):
    global repo_path
    global activeIssues
    
    activeIssues = []
    
    commitType = type.get()
    commitScope = f"({issueBox.get()})" if issue.instate(['selected']) else ''
    if issue.instate(['selected']):
        issue.invoke()
    commitBreakingChange = '!' if breakingChange.instate(['selected']) else ''
    if breakingChange.instate(['selected']):
        breakingChange.invoke()
    commitMessage = message.get()
    commitBody = f"-m \'{bodyText.get()}\'" if body.instate(['selected']) else ''
    if body.instate(['selected']):
        body.invoke()
    commitFooter = f"-m \'BREAKING CHANGE: {breakingChangeFooterText.get()}\'" if breakingChangeFooter.instate(['selected']) else ""
    if breakingChangeFooter.instate(['selected']):
        breakingChangeFooter.invoke()

    commit = f'git commit -m \'{commitType}{commitScope}{commitBreakingChange}: {commitMessage}\' {commitBody} {commitFooter}'

    # Run the git commit command in the selected repository path
    try:
        subprocess.run("git add .", shell=True, check=True, cwd=repo_path)
        subprocess.run(commit, shell=True, check=True, cwd=repo_path)
        root.clipboard_clear()
        root.clipboard_append(commit)
        show_toast("Commit successfully created", 3000, True)
        issues = getIssues()
        for i in issues:
            activeIssues.append({
                "title": i["title"],
                "number": i["number"]
            })
        update_combobox()
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode('utf-8') if e.stderr else str(e)
        root.clipboard_clear()
        root.clipboard_append(error_message)
        show_toast(f"{error_message}", 3000, False)

    type.set('')
    issueBox.set('')
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

# def createProject():
#     newProjectName = newProject.get()
#     if newProjectName:
#         newProjectDict = {
#             "name": newProjectName,
#             "scopes": []
#         }
#         projects.append(newProjectDict)
#         names.append(newProjectName)
#         projectSelect["values"] = names
#         project["values"] = names
#         newProject.delete(0, tk.END)
#         projectSelect.current(len(names) - 1)
#         update_combobox2()
#         saveProjectsToFile(projects)

# def createScope():
#     newScopeName = newScope.get()
#     projectAddScope = projectSelect.get()
#     for i in projects:
#         if projectAddScope == i["name"]:
#             i["scopes"].append(newScopeName)
#             update_combobox2()
#             break

#     newScope.delete(0, tk.END)
#     saveProjectsToFile(projects)

# def deleteScope():
#     scopeToDelete = scopeBox3.get()
#     selectedProject = projectSelect.get()

#     for project in projects:
#         if project["name"] == selectedProject:
#             if scopeToDelete in project["scopes"]:
#                 project["scopes"].remove(scopeToDelete)
#                 update_combobox2()
#                 break

#     scopeBox3.set('')
#     saveProjectsToFile(projects)

# def editProjectName():
#     selected_project_name = projectSelect.get()
#     new_project_name = newProject.get()

#     if selected_project_name and new_project_name:
#         for project in projects:
#             if project["name"] == selected_project_name:
#                 project["name"] = new_project_name
#                 break

#         saveProjectsToFile(projects)
#         newProject.delete(0, tk.END)
#         names[names.index(selected_project_name)] = new_project_name
#         projectSelect["values"] = names
#         projectSelect.set(new_project_name)
#         project.set(new_project_name)
#         update_combobox2()

def show_toast(message, duration=3000, state=True):
    color = ""
    
    if state:
        color = "success"
    else:
        color = "danger"
    
    toast = tk.Toplevel()
    toast.wm_overrideredirect(True)
    toast.attributes("-topmost", True)

    label = ttk.Label(toast, text=message, bootstyle=color, padding=10, )
    label.pack()

    x = (toast.winfo_screenwidth() // 2) - (toast.winfo_reqwidth() // 2)
    y = toast.winfo_screenheight() - 100
    toast.geometry(f"+{x}+{y}")

    toast.after(duration, toast.destroy)

#----------Frame 1 (Commits Functions)----------#
root = ttkb.Window(themename="solar")
root.title("Conventional Commits Tool")
root.geometry('350x600')
root.resizable(False, False)

#Style Object
style = ttkb.Style()
style.configure(
    "Custom.TSeparator", 
    background=root.style.colors.primary,
    thickness=1,
    relief="solid",
)

frm = ttkb.Frame(root, padding=10, bootstyle="default")
frm.grid(sticky='nsew')
frm.columnconfigure(1, weight=1, uniform="equal")
frm.columnconfigure(2, weight=1, uniform="equal")

#Row 0 (Frame Buttons)
ttkb.Button(frm, text="Commit", command=show_commit_frame, bootstyle="primary-outline").grid(column=1, row=0, sticky='w', padx=5, pady=5)
ttkb.Button(frm, text="Issues", command=show_project_frame, bootstyle="primary-outline").grid(column=2, row=0, sticky='w', padx=5, pady=5)

#Row 1 (Separator)
ttk.Separator(frm, orient='horizontal', style='Custom.TSeparator').grid(column=1, row=1, sticky='ew', pady=(20, 10))


#Row 2 (Selected repo path label and button)
repoPathLabel = ttkb.Label(frm, text="Select a repo path", bootstyle="dark", foreground="white", wraplength=300)
repoPathLabel.grid(columnspan=3, row=2, sticky='w', padx=5, pady=5)
ttkb.Button(frm, text="Select Repo Path", command=selectRepoPath, bootstyle="primary-outline").grid(column=2, row=2, sticky='w', padx=5, pady=5)

#Row 3 (Repo path label and button)
ttkb.Label(frm, text="Project Template", bootstyle="dark", foreground="white").grid(column=1, row=3, sticky='w', padx=5, pady=5)
ttkb.Button(frm, text="Change Directory", command=changeDirectory, bootstyle="primary-outline").grid(column=2, row=3, sticky='w', padx=5, pady=5)

#Row 4 (Separator)
ttk.Separator(frm, orient='horizontal', style='Custom.TSeparator').grid(columnspan=3, row=4, sticky='ew', pady=(20, 10))

#Row 5 (Type Label)
ttkb.Label(frm, text="Type", bootstyle="dark", foreground="white").grid(column=1, row=5, sticky='w', padx=5, pady=5)

#Row 6 (Type select and breaking change toggle)
breakingChange = ttkb.Checkbutton(frm, text="Breaking Change", command=enableBreakingChange, bootstyle="primary-round-toggle")
breakingChange.grid(column=2, row=6, sticky='w', padx=5, pady=5)
breakingChange.invoke()
breakingChange.invoke()
type = ttkb.Combobox(frm, state="readonly", values=["build", "chore", "ci", "docs", "feat", "fix", "perf", "refactor", "revert", "style", "test"], bootstyle="primary", foreground="white")
type.grid(column=1, row=6, sticky='w', padx=5, pady=5)

#Row 7 (Scope label and selection)
issue = ttkb.Checkbutton(frm, text="Issue", command=enableIssue, bootstyle="primary-round-toggle")
issue.grid(column=1, row=7, sticky='w', padx=5, pady=5)
issue.invoke()
issue.invoke()
issueBox = ttkb.Combobox(frm, state="readonly", values=[], bootstyle="dark", foreground="white")
issueBox.grid(column=2, row=7, sticky='w', padx=5, pady=5)

#Row 8 (Message label)
ttkb.Label(frm, text="Message", bootstyle="dark", foreground="white").grid(column=1, row=8, sticky='w', padx=5, pady=5)

#Row 9 (Message entry)
message = ttkb.Entry(frm, bootstyle="primary" ,foreground="white")
message.grid(column=1, row=9, sticky='w', padx=5, pady=5)

#Row 10 (Body entry and toggle)
body = ttkb.Checkbutton(frm, text="Body", command=enableBody, bootstyle="primary-round-toggle")
body.grid(column=1, row=10, sticky='w', padx=5, pady=5)
body.invoke()
body.invoke()
bodyText = ttkb.Entry(frm, bootstyle="dark",foreground="white")
bodyText.grid(column=2, row=10, sticky='w', padx=5, pady=5)

#Row 11 (Breaking change Footer entry and toggle)
breakingChangeFooter = ttkb.Checkbutton(frm, text="Breaking Change Footer", command=enableBreakingChangeFooter, bootstyle="primary-round-toggle")
breakingChangeFooter.grid(column=1, row=11, sticky='w', padx=5, pady=5)
breakingChangeFooter.invoke()
breakingChangeFooter.invoke()
breakingChangeFooterText = ttkb.Entry(frm, bootstyle="dark", foreground="white")
breakingChangeFooterText.grid(column=2, row=11, sticky='w', padx=5, pady=5)

#Row 12 (Separator)
ttk.Separator(frm, orient='horizontal', style='Custom.TSeparator').grid(columnspan=3, row=12, sticky='ew', pady=(20, 10))

#Row 13 (Create commit button)
ttkb.Button(frm, text="Create Commit", command=createCommitMessage, bootstyle="success-outline").grid(column=1, row=13, sticky='w', padx=5, pady=5)

breakingChangeFooterText.config(state='disabled')
breakingChangeFooterText.configure(bootstyle='disabled')
bodyText.config(state='disabled')
bodyText.configure(bootstyle='disabled')
issueBox.config(state='disabled')
breakingChangeFooter.config(state='disabled')
breakingChangeFooterText.config(state='disabled')

#----------Frame 2 (Project Functions)----------#
frm2 = ttkb.Frame(root, padding=10, bootstyle="default")
frm2.columnconfigure(1, weight=1, uniform="equal")
frm2.columnconfigure(2, weight=1, uniform="equal")

#Row 0 (Frame Buttons)
ttkb.Button(frm2, text="Commit", command=show_commit_frame, bootstyle="primary-outline").grid(column=1, row=0, sticky='w', padx=5, pady=5)
ttkb.Button(frm2, text="Issues", command=show_project_frame, bootstyle="primary-outline").grid(column=2, row=0, sticky='w', padx=5, pady=5)

#Row 1 (Separator)
ttk.Separator(frm2, orient='horizontal', style='Custom.TSeparator').grid(columnspan=3, row=1, sticky='ew', pady=(5, 10))

#Row 2 (Repo Owner Label)
ttkb.Label(frm2, text="Repo owner", bootstyle="dark", foreground="white").grid(column=1, row=2, sticky='w', padx=5, pady=5)

#Row 3 (Button to save repo owner)
repo_owner = ttkb.Button(frm2, text="Autodetect Repo Owner", command=get_repo_owner, bootstyle="primary-outline")
repo_owner.grid(column=1, row=3, sticky='w', padx=5, pady=5)
repo_user = ttkb.Entry(frm2, bootstyle="primary", foreground="white")
repo_user.grid(column=2, row=3, sticky='w', padx=5, pady=5)

#Row 4 (Repo name label)
ttkb.Label(frm2, text="Repo Name", bootstyle="dark", foreground="white").grid(column=1, row=4, sticky='w', padx=5, pady=5)

#Row 5 (Repo name entry and autodetect button)
repo_name_entry = ttkb.Entry(frm2, bootstyle="primary", foreground="white")
repo_name_entry.grid(column=2, row=5, sticky='w', padx=5, pady=5)
repo_name_autodetect = ttkb.Button(frm2, text="Autodetect Repo Name", command=get_repo_name, bootstyle="primary-outline")
repo_name_autodetect.grid(column=1, row=5, sticky='w', padx=5, pady=5)

#Row 6 (Save Button)
save_info = ttkb.Button(frm2, text="Save Repo Info", command=updateRepoInfo, bootstyle="success-outline")
save_info.grid(column=1, row=6, sticky='w', padx=5, pady=5)

#Row 7 (Separator)
ttk.Separator(frm2, orient='horizontal', style='Custom.TSeparator').grid(columnspan=3, row=7, sticky='ew', pady=(5, 10))

# #Row 0 (Frame Buttons)
# ttkb.Button(frm2, text="Commit", command=show_commit_frame, bootstyle="primary-outline").grid(column=1, row=0, sticky='w', padx=5, pady=5)
# ttkb.Button(frm2, text="Projects", command=show_project_frame, bootstyle="primary-outline").grid(column=2, row=0, sticky='w', padx=5, pady=5)

# #Row 1 (Separator)
# ttk.Separator(frm2, orient='horizontal', style='Custom.TSeparator').grid(columnspan=3, row=1, sticky='ew', pady=(5, 10))

# #Row 2 (Project selection)
# ttkb.Label(frm2, text="Project Template", bootstyle="dark", foreground="white").grid(column=1, row=2, sticky='w', padx=5, pady=5)
# projectSelect = ttkb.Combobox(frm2, state="readonly", values=names, bootstyle="primary", foreground="white")
# projectSelect.grid(column=2, row=2, sticky='w', padx=5, pady=5)
# projectSelect.bind("<<ComboboxSelected>>", update_combobox2)

# #Row 3 (Project name entry and Project creation button)
# generateProject = ttkb.Button(frm2, text="Create Project Template", command=createProject, bootstyle="primary-outline")
# generateProject.grid(column=2, row=3, sticky='w', padx=5, pady=5)
# newProject = ttkb.Entry(frm2, bootstyle="primary", foreground="white")
# newProject.grid(column=1, row=3, sticky='w', padx=5, pady=5)

# #Row 4 (Edit project button)
# editProject = ttkb.Button(frm2, text="Edit Project Name", command=editProjectName, bootstyle="primary-outline")
# editProject.grid(column=2, row=4, sticky='w', padx=5, pady=5)

# #Row 5 (Add scopes label)
# ttkb.Label(frm2, text="Add Scopes", bootstyle="dark", foreground="white").grid(column=1, row=5, sticky='w', padx=5, pady=5)

# #Row 6 (Adding scopes entry and button)
# newScope = ttkb.Entry(frm2, bootstyle="primary", foreground="white")
# newScope.grid(column=1, row=6, sticky='w', padx=5, pady=5)
# generateScope = ttkb.Button(frm2, text="Add Scope", command=createScope, bootstyle="primary-outline")
# generateScope.grid(column=2, row=6, sticky='w', padx=5, pady=5)

# #Row 7 (Delete scopes label)
# ttkb.Label(frm2, text="Delete Scopes", bootstyle="dark", foreground="white").grid(column=1, row=7, sticky='w', padx=5, pady=5)

# #Row 8 (Delete scopes select and button)
# scopeBox3 = ttkb.Combobox(frm2, state="readonly", values=[], bootstyle="primary", foreground="white")
# scopeBox3.grid(column=1, row=8, sticky='w', padx=5, pady=5)
# deleteScope = ttkb.Button(frm2, text="Delete Scope", command=deleteScope, bootstyle="primary-outline")
# deleteScope.grid(column=2, row=8, sticky='w', padx=5, pady=5)

#Showing the first frame
frm.grid(sticky='nsew')

# Initialize the window
root.mainloop()

#----------Functions----------#
