import tkinter
from tkinter import ttk

import internal.objects.interfaces
import internal.view.dependencies


class Window(tkinter.Toplevel):
    def __init__(self,
                 dependencies: internal.view.dependencies.Dependencies,
                 canvas: bool = False
                 ):
        super(Window, self).__init__(dependencies.canvas)
        self.dependencies = dependencies
        # self.window = dependencies.canvas
        if canvas:
            self.canvas = tkinter.Canvas(self, width=1200, height=600, bg='white')
            self.canvas.pack(expand=False)

        self.entries = dict()
        self.saved = False

    def add_entry(self, name):
        self.entries[name] = ttk.Entry(self)
        return self.entries[name]

    def add_combobox(self, name, vals):
        self.entries[name] = ttk.Combobox(self, values=vals, state='readonly')
        return self.entries[name]

    def get_vals(self):
        if self.saved:
            tmp = dict()
            for name, entry in self.entries.items():
                tmp[name] = entry.get()
            return tmp
        return None
