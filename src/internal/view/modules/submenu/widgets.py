import tkinter
from tkinter import ttk
from typing import List

import internal.objects.interfaces
import internal.view.dependencies
import internal.view.utils
from internal.view.utils import get_font_colors


def font_color_widget(
    dependencies: internal.view.dependencies.Dependencies,
    obj_id: internal.objects.interfaces.ObjectId
) -> List[ttk.Widget]:
    string_var = tkinter.StringVar()
    restrictions = get_font_colors()
    label = ttk.Label(
        dependencies.property_bar,
        text='Цвет шрифта',
        justify='left',
        anchor='w'
    )
    combobox = tkinter.ttk.Combobox(
        dependencies.property_bar,
        textvariable=string_var,
        values=restrictions,
        state='readonly'
    )
    string_var.trace('w', lambda *_: _set_font_color(
        dependencies, obj_id, string_var.get()
    ))
    combobox.current(restrictions.index(_get_font_color(
        dependencies, obj_id
    )))
    return label, combobox


def _get_font_color(
    dependencies: internal.view.dependencies.Dependencies,
    obj_id: internal.objects.interfaces.ObjectId,
):
    return dependencies.canvas.itemcget(obj_id, 'fill')


def _set_font_color(
    dependencies: internal.view.dependencies.Dependencies,
    obj_id: internal.objects.interfaces.ObjectId,
    font_color: str
):
    dependencies.canvas.itemconfig(obj_id, fill=font_color)
    dependencies.controller.edit_font_color(obj_id, font_color)
