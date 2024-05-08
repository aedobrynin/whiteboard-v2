import tkinter
from tkinter import ttk

import internal.objects.interfaces
import internal.view.dependencies
# from internal.models.attribute import Attribute

def open_window(
    dependencies: internal.view.dependencies.Dependencies
) -> (tkinter.Toplevel, ttk.Entry):
    window = tkinter.Toplevel(dependencies.canvas)
    window.title('New attribute')

    label = ttk.Label(window, text='Name')
    label.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    entry = ttk.Entry(window)
    entry.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
    return window, entry

def get_values(window, entry) -> str:
    name = None

    def after_add():
        nonlocal name
        name = entry.get()
        window.destroy()

    bt = ttk.Button(window, text='Save', command=after_add)
    bt.grid(row=4, column=1, padx=5, pady=5, sticky='nsew')
    return name


