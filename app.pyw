import os
import jsonreader
import tkinter as tk
from tkinter import ttk

projects = jsonreader.downloadScopes()
names = [project["name"] for project in projects]

stateBreakingChange = False
stateBreakingChangeFooter = False
stateBody = False
stateScope = False

def update_combobox(*args):
    selected_value = project.get()
    for i in projects:
        if selected_value == i["name"]:
            scopeBox["values"] = i["scopes"]
            scopeBox.current(0)
            break

def enableBreakingChange():
    if(breakingChange.instate(['selected']) != True):
        breakingChangeFooter.config(state='disabled')
        breakingChangeFooterText.config(state='disabled')
        stateBreakingChange = False
    else:
        breakingChangeFooter.config(state='normal')
        breakingChangeFooterText.config(state='normal')
        stateBreakingChange = True

def enableScope():
    if(scope.instate(["selected"]) != True):
        scopeBox.config(state='disabled')
        stateScope = False
    else:
        scopeBox.config(state='normal')
        stateScope = True

def enableBody():
    if(body.instate(["selected"]) != True):
        bodyText.config(state='disabled')
        stateBody = False
    else:
        bodyText.config(state='normal')
        stateBody = True

def enableBreakingChangeFooter():
    if(breakingChangeFooter.instate(["selected"]) != True):
        breakingChangeFooterText.config(state='disabled')
        stateBreakingChangeFooter = False
    else:
        breakingChangeFooterText.config(state='normal')
        stateBreakingChangeFooter = True

def createCommitMessage():
    commitType = ""
    commitScope = ""
    commitBreakingChange = ""
    commitMessage = ""
    commitBody = ""
    commitFooter = ""

root = tk.Tk()
root.title("Conventional Commits Tool")
root.geometry('600x450')
root.resizable(False, False)

frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Button(frm, text="Commit", command=root.destroy).grid(column=1, row=0)
ttk.Button(frm, text="Projects", command=root.destroy).grid(column=2, row=0)

ttk.Label(frm, text="Type").grid(column=1, row=2)
breakingChange = ttk.Checkbutton(frm, text="Breaking Change", command=enableBreakingChange)
breakingChange.grid(column=2, row=3)
type = ttk.Combobox(frm, state="readonly", values=["build", "chore", "ci", "docs", "feat", "fix", "perf", "refactor", "revert", "style", "test"])
type.grid(column=1, row=3)

scope = ttk.Checkbutton(frm, text="Scope", command=enableScope)
scope.grid(column=1, row=6)
scopeBox = ttk.Combobox(frm, state="readonly", values=[])
scopeBox.grid(column=2, row=6)

ttk.Label(frm, text="Message").grid(column=1, row=7)
ttk.Entry(frm).grid(column=1, row=8)

body = ttk.Checkbutton(frm, text="Body", command=enableBody)
body.grid(column=1, row=10)
bodyText = ttk.Entry(frm)
bodyText.grid(column=2, row=10)

breakingChangeFooter = ttk.Checkbutton(frm, text="Breaking Change Footer", command=enableBreakingChangeFooter)
breakingChangeFooter.grid(column=1, row=12)
breakingChangeFooterText = ttk.Entry(frm)
breakingChangeFooterText.grid(column=2, row=12)

ttk.Label(frm, text="Project Template").grid(column=1, row=1)
project = ttk.Combobox(frm, state="readonly", values=names)
project.grid(column=2, row=1)

project.bind("<<ComboboxSelected>>", update_combobox)

root.mainloop()
