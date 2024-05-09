# import tkinter
# from tkinter import ttk
# from typing import List, Callable
#
# import internal.objects.interfaces
# import internal.view.dependencies
# import internal.view.utils
# from internal.view.utils.props_values import (
#     get_text_line_widths,
#     get_font_colors,
# )
#
# from .view import PEN_LINE_PREFIX
#
#
# def widgets(
#     dependencies: internal.view.dependencies.Dependencies,
#     obj_id: internal.objects.interfaces.ObjectId
# ) -> List[ttk.Widget]:
#     _widgets = []
#     for func in _widgets_func():
#         label, combobox = func(dependencies, obj_id)
#         _widgets.append(label)
#         _widgets.append(combobox)
#     return _widgets
#
#
# def _widgets_func() -> List[Callable]:
#     return [
#         lambda dependencies, obj_id: _base_widget(
#             dependencies,
#             obj_id,
#             get_font_colors(),
#             'Цвет',
#             _get_color,
#             _set_color
#         ),
#         lambda dependencies, obj_id: _base_widget(
#             dependencies,
#             obj_id,
#             get_text_line_widths(),
#             'Толщина',
#             _get_width,
#             _set_width
#         )
#     ]
#
#
# def _base_widget(
#     dependencies: internal.view.dependencies.Dependencies,
#     obj_id: internal.objects.interfaces.ObjectId,
#     restrictions: List,
#     description: str,
#     getter: Callable,
#     setter: Callable
# ) -> List[ttk.Widget]:
#     string_var = tkinter.StringVar()
#     label = ttk.Label(
#         dependencies.property_bar,
#         text=description,
#         justify='left',
#         anchor='w'
#     )
#     combobox = tkinter.ttk.Combobox(
#         dependencies.property_bar,
#         textvariable=string_var,
#         values=restrictions,
#         state='readonly'
#     )
#     string_var.trace('w', lambda *_: setter(
#         dependencies, obj_id, string_var.get()
#     ))
#     combobox.current(restrictions.index(getter(
#         dependencies, obj_id
#     )))
#     return label, combobox
#
#
# def _get_width(
#     dependencies: internal.view.dependencies.Dependencies,
#     obj_id: internal.objects.interfaces.ObjectId,
# ):
#     return int(float(dependencies.canvas.itemcget(PEN_LINE_PREFIX + obj_id, 'width')))
#
#
# def _set_width(
#     dependencies: internal.view.dependencies.Dependencies,
#     obj_id: internal.objects.interfaces.ObjectId,
#     width: float
# ):
#     dependencies.canvas.itemconfig(PEN_LINE_PREFIX + obj_id, width=width)
#     dependencies.controller.edit_width(obj_id, width=width)
#
#
# def _get_color(
#     dependencies: internal.view.dependencies.Dependencies,
#     obj_id: internal.objects.interfaces.ObjectId,
# ):
#     return dependencies.canvas.itemcget(PEN_LINE_PREFIX + obj_id, 'fill')
#
#
# def _set_color(
#     dependencies: internal.view.dependencies.Dependencies,
#     obj_id: internal.objects.interfaces.ObjectId,
#     color: str
# ):
#     dependencies.canvas.itemconfig(PEN_LINE_PREFIX + obj_id, fill=color)
#     dependencies.controller.edit_color(obj_id, color=color)
