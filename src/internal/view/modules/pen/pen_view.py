from __future__ import annotations

import tkinter
import tkinter.font
import tkinter.ttk
from typing import List, Callable

import internal.objects.interfaces
import internal.objects.events
import internal.repositories.interfaces
import internal.view.dependencies
import internal.view.objects.interfaces
from internal.view.objects.impl.object import ViewObject
from internal.view.consts import VIEW_OBJECT_ID
from internal.view.utils import get_line_widths, get_font_colors

_LINE_WIDTH_DESC = 'Толщина линии'
_LINE_COLOR_DESC = 'Цвет линии'


class PenObject(ViewObject):
    def __init__(
        self,
        dependencies: internal.view.dependencies.Dependencies,
        obj: internal.objects.interfaces.IBoardObjectPen,
    ):
        ViewObject.__init__(self, dependencies, obj)
        self._line_id = dependencies.canvas.create_line(
            self._get_canvas_points_from_repo_object(dependencies),
            width=obj.width,
            fill=obj.color,
            capstyle=tkinter.ROUND,
            smooth=True,
            tags=[obj.id],
        )
        self._subscribe_to_change_color(dependencies)
        self._subscribe_to_change_width(dependencies)
        self._subscribe_to_change_points(dependencies)
        self._subscribe_to_change_move(dependencies)

    @property
    def line_id(self):
        return self._line_id

    def _get_canvas_points_from_repo_object(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        obj: internal.objects.interfaces.IBoardObjectPen = dependencies.repo.get(self.id)
        points = []
        for position in obj.points:
            points.append(position.x)
            points.append(position.y)
        return points

    def _subscribe_to_change_color(self, dependencies: internal.view.dependencies.Dependencies):
        dependencies.pub_sub_broker.subscribe(
            VIEW_OBJECT_ID,
            self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_COLOR,
            lambda publisher, event, repo: self._get_color_update_from_repo(dependencies),
        )

    def _get_color_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectPen = dependencies.repo.get(self.id)
        dependencies.canvas.itemconfigure(self.line_id, fill=obj.color)

    def _subscribe_to_change_width(self, dependencies: internal.view.dependencies.Dependencies):
        dependencies.pub_sub_broker.subscribe(
            VIEW_OBJECT_ID,
            self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_WIDTH,
            lambda publisher, event, repo: self._get_width_update_from_repo(dependencies),
        )

    def _get_width_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectPen = dependencies.repo.get(self.id)
        dependencies.canvas.itemconfigure(self.line_id, width=obj.width)

    def _subscribe_to_change_points(self, dependencies: internal.view.dependencies.Dependencies):
        dependencies.pub_sub_broker.subscribe(
            VIEW_OBJECT_ID,
            self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_POINTS,
            lambda publisher, event, repo: dependencies.canvas.coords(
                self.line_id, self._get_canvas_points_from_repo_object(dependencies)
            ),
        )

    def _subscribe_to_change_move(self, dependencies: internal.view.dependencies.Dependencies):
        dependencies.pub_sub_broker.subscribe(
            VIEW_OBJECT_ID,
            self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_MOVED,
            lambda publisher, event, repo: dependencies.canvas.coords(
                self.line_id, self._get_canvas_points_from_repo_object(dependencies)
            ),
        )

    def widgets(
        self, dependencies: internal.view.dependencies.Dependencies
    ) -> List[tkinter.ttk.Widget]:
        _widgets = []
        for func in self._widgets_func():
            label, combobox = func(dependencies)
            _widgets.append(label)
            _widgets.append(combobox)
        return _widgets

    def _widgets_func(self) -> List[Callable]:
        return [
            lambda dependencies: self._base_widget(
                dependencies, get_font_colors(), _LINE_COLOR_DESC, self._get_color, self._set_color
            ),
            lambda dependencies: self._base_widget(
                dependencies, get_line_widths(), _LINE_WIDTH_DESC, self._get_width, self._set_width
            ),
        ]

    def _base_widget(
        self,
        dependencies: internal.view.dependencies.Dependencies,
        restrictions: List,
        description: str,
        getter: Callable,
        setter: Callable,
    ) -> List[tkinter.ttk.Widget]:
        string_var = tkinter.StringVar()
        label = tkinter.ttk.Label(
            dependencies.property_bar, text=description, justify='left', anchor='w'
        )
        combobox = tkinter.ttk.Combobox(
            dependencies.property_bar,
            textvariable=string_var,
            values=restrictions,
            state='readonly',
        )
        combobox.current(restrictions.index(getter(dependencies)))
        string_var.trace('w', lambda *_: setter(dependencies, string_var.get()))
        return label, combobox

    def _get_color(self, dependencies: internal.view.dependencies.Dependencies):
        return dependencies.canvas.itemcget(self.line_id, 'fill')

    def _set_color(self, dependencies: internal.view.dependencies.Dependencies, color: str):
        dependencies.controller.edit_color(self.id, color=color)

    def _get_width(self, dependencies: internal.view.dependencies.Dependencies):
        return int(float(dependencies.canvas.itemcget(self.line_id, 'width')))

    def _set_width(self, dependencies: internal.view.dependencies.Dependencies, width: int):
        dependencies.controller.edit_width(self.id, width=width)
