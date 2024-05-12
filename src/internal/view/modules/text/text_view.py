from __future__ import annotations

import logging
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

from internal.view.utils import (
    get_font_families,
    get_font_weights,
    get_font_slants,
    get_font_colors,
    get_font_sizes,
    as_tkinter_object_font,
    as_object_font,
)

_FONT_FAMILY_DESC = 'Шрифт'
_FONT_SLANT_DESC = 'Наклон шрифта'
_FONT_WEIGHT_DESC = 'Насыщенность шрифта'
_FONT_SIZE_DESC = 'Размер шрифта'
_FONT_COLOR_DESC = 'Цвет шрифта'


class TextObject(ViewObject):
    def __init__(
        self,
        dependencies: internal.view.dependencies.Dependencies,
        obj: internal.objects.interfaces.IBoardObjectText,
    ):
        ViewObject.__init__(self, dependencies, obj)
        self._text_id = dependencies.canvas.create_text(
            obj.position.x,
            obj.position.y,
            text=obj.text,
            fill=obj.font.color,
            tags=[obj.id],
            font=(obj.font.family, int(obj.font.size), obj.font.weight, obj.font.slant),
        )
        self._subscribe_to_change_font(dependencies)
        self._subscribe_to_change_text(dependencies)
        self._subscribe_to_change_move(dependencies)

    @property
    def text_id(self):
        return self._text_id

    def _subscribe_to_change_font(self, dependencies: internal.view.dependencies.Dependencies):
        dependencies.pub_sub_broker.subscribe(
            VIEW_OBJECT_ID,
            self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_FONT,
            lambda publisher, event, repo: self.get_font_update_from_repo(dependencies),
        )

    def _subscribe_to_change_text(self, dependencies: internal.view.dependencies.Dependencies):
        dependencies.pub_sub_broker.subscribe(
            VIEW_OBJECT_ID,
            self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_TEXT,
            lambda publisher, event, repo: self.get_text_update_from_repo(dependencies),
        )

    def _subscribe_to_change_move(self, dependencies: internal.view.dependencies.Dependencies):
        dependencies.pub_sub_broker.subscribe(
            VIEW_OBJECT_ID,
            self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_MOVED,
            lambda publisher, event, repo: self.get_move_update_from_repo(dependencies),
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
                dependencies,
                get_font_families(),
                _FONT_FAMILY_DESC,
                self.get_font_family,
                self.set_font_family,
            ),
            lambda dependencies: self._base_widget(
                dependencies,
                get_font_slants(),
                _FONT_SLANT_DESC,
                self.get_font_slant,
                self.set_font_slant,
            ),
            lambda dependencies: self._base_widget(
                dependencies,
                get_font_weights(),
                _FONT_WEIGHT_DESC,
                self.get_font_weight,
                self.set_font_weight,
            ),
            lambda dependencies: self._base_widget(
                dependencies,
                get_font_sizes(),
                _FONT_SIZE_DESC,
                self.get_font_size,
                self.set_font_size,
            ),
            lambda dependencies: self._base_widget(
                dependencies,
                get_font_colors(),
                _FONT_COLOR_DESC,
                self.get_font_color,
                self.set_font_color,
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

    def get_font_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        logging.debug('canvas font to update')
        obj: internal.objects.interfaces.IBoardObjectText = dependencies.repo.get(self.id)
        font = obj.font
        tk_font = as_tkinter_object_font(font)
        dependencies.canvas.itemconfigure(self.text_id, font=tk_font)
        dependencies.canvas.itemconfigure(self.text_id, fill=font.color)

    def get_text_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectText = dependencies.repo.get(self.id)
        dependencies.canvas.itemconfigure(self.text_id, text=obj.text)

    def get_move_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectText = dependencies.repo.get(self.id)
        self.move_to(dependencies, obj.position.x, obj.position.y)

    def get_font(self, dependencies: internal.view.dependencies.Dependencies):
        font = dependencies.canvas.itemcget(self.text_id, 'font')
        color = dependencies.canvas.itemcget(self.text_id, 'fill')
        return as_object_font(font, color)

    def get_font_slant(self, dependencies: internal.view.dependencies.Dependencies):
        return self.get_font(dependencies).slant

    def set_font_slant(self, dependencies: internal.view.dependencies.Dependencies, value: str):
        font = self.get_font(dependencies)
        font.slant = value
        dependencies.controller.edit_font(self.id, font=font)

    def get_font_weight(self, dependencies: internal.view.dependencies.Dependencies):
        return self.get_font(dependencies).weight

    def set_font_weight(self, dependencies: internal.view.dependencies.Dependencies, value: str):
        font = self.get_font(dependencies)
        font.weight = value
        dependencies.controller.edit_font(self.id, font=font)

    def get_font_family(self, dependencies: internal.view.dependencies.Dependencies):
        return self.get_font(dependencies).family

    def set_font_family(self, dependencies: internal.view.dependencies.Dependencies, value: str):
        font = self.get_font(dependencies)
        font.family = value
        dependencies.controller.edit_font(self.id, font=font)

    def get_font_size(self, dependencies: internal.view.dependencies.Dependencies):
        return int(self.get_font(dependencies).size)

    def set_font_size(self, dependencies: internal.view.dependencies.Dependencies, value: str):
        font = self.get_font(dependencies)
        font.size = int(value)
        dependencies.controller.edit_font(self.id, font=font)

    def get_font_color(self, dependencies: internal.view.dependencies.Dependencies):
        return self.get_font(dependencies).color

    def set_font_color(self, dependencies: internal.view.dependencies.Dependencies, color: str):
        font = self.get_font(dependencies)
        font.color = color
        dependencies.controller.edit_font(self.id, font=font)
