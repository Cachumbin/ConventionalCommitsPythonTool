import os
import jsonreader
from tkinter import *
from tkinter import ttk

projects = jsonreader.downloadScopes()

def update_combobox(*args):
    selected_value = project.get()
    for i in projects:
        if(selected_value == i["name"]):
            scope["values"] = i["scopes"]
            scope.current(0)
            break

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
scope = ttk.Combobox(state="readonly", values=[]).grid(column=2, row=6)

ttk.Label(frm, text="Message").grid(column=1, row=7)
ttk.Entry(frm).grid(column=1, row=8)

ttk.Label(frm, text="Body").grid(column=1, row=9)
ttk.Checkbutton(frm).grid(column=1,row=10)
ttk.Entry(frm).grid(column=2, row=10)

ttk.Label(frm, text="Breaking Change Footer").grid(column=1, row=11)
ttk.Checkbutton(frm).grid(column=1,row=12)
ttk.Entry(frm).grid(column=2, row=12)

ttk.Label(frm, text="Project Template").grid(column=1, row=1)
templates = [i['name'] for i in projects]
project = ttk.Combobox(state="readonly", values=templates)
project.grid(column=2, row=1)

project.bind("<<ComboboxSelected>>", update_combobox)

root.mainloop()