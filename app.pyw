import os
import jsonreader
from tkinter import *
from tkinter import ttk

scopes = []

def getScopes(self):

    for project in projects:
        if(project["name"] == self.get()):
            scope["values"] = [project["name"]]

projects = jsonreader.downloadScopes()

names = []



for project in projects:
    names.append(project["name"])

root = Tk()
root.title("Conventional Commits Tool")

frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Button(frm, text="Commit", command=root.destroy).grid(column=1, row=0)
ttk.Button(frm, text="Projects", command=root.destroy).grid(column=2, row=0)

ttk.Label(frm, text="Type").grid(column=1, row=2)
ttk.Checkbutton(frm, text="Breaking Change").grid(column=2,row=3)
ttk.Combobox(state="readonly", values=["build", "chore", "ci", "docs", "feat", "fix", "perf", "refactor", "revert", "style", "test"]).grid(column=1, row=3)
ttk.Label(frm, text="Scope").grid(column=1, row=4)
ttk.Checkbutton(frm).grid(column=2, row=4)

ttk.Label(frm, text="Scope").grid(column=2, row=5)
scope = ttk.Combobox(state="readonly", values=scopes).grid(column=2, row=6)

ttk.Label(frm, text="Message").grid(column=1, row=7)
ttk.Entry(frm).grid(column=1, row=8)

ttk.Label(frm, text="Body").grid(column=1, row=9)
ttk.Checkbutton(frm).grid(column=1,row=10)
ttk.Entry(frm).grid(column=2, row=10)

ttk.Label(frm, text="Breaking Change Footer").grid(column=1, row=11)
ttk.Checkbutton(frm).grid(column=1,row=12)
ttk.Entry(frm).grid(column=2, row=12)

ttk.Label(frm, text="Project Template").grid(column=1, row=1)
project = ttk.Combobox(state="readonly", values=names).grid(column=2, row=1)
ttk.Button(frm, text="Done", command=getScopes).grid(column=3, row=1)

root.mainloop()