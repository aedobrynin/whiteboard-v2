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
from internal.view.objects.impl import ViewObject
from internal.view.consts import VIEW_OBJECT_ID

from internal.view.utils import (
    get_font_families,
    get_font_weights,
    get_font_slants,
    get_font_colors,
    get_card_sizes,
    as_tkinter_object_font,
    as_object_font,
)

_DEFAULT_SMALL_SIZE = 150
_DEFAULT_MEDIUM_SIZE = 250
_DEFAULT_LARGE_SIZE = 350
_FONT_FAMILY_DESC = 'Шрифт'
_FONT_SLANT_DESC = 'Наклон шрифта'
_FONT_WEIGHT_DESC = 'Насыщенность шрифта'
_FONT_SIZE_DESC = 'Размер шрифта'
_FONT_COLOR_DESC = 'Цвет шрифта'
_CARD_COLOR_DESC = 'Цвет карточки'


class CardObject(ViewObject):
    def __init__(
        self,
        dependencies: internal.view.dependencies.Dependencies,
        obj: internal.objects.interfaces.IBoardObjectCard,
    ):
        ViewObject.__init__(self, dependencies, obj)
        width = obj.dimension[0]
        height = obj.dimension[1]
        self._note_id = dependencies.canvas.create_rectangle(
            obj.position.x,
            obj.position.y,
            obj.position.x + width,
            obj.position.y + height,
            fill=obj.color,
            tags=[obj.id],
        )

        self._text_id = dependencies.canvas.create_text(
            obj.position.x + width / 2,
            obj.position.y + height / 2,
            text=obj.text,
            fill=obj.font.color,
            tags=[obj.id],
            width=width,
            font=(obj.font.family, int(obj.font.size), obj.font.weight, obj.font.slant),
        )
        self.adjust_font(dependencies)
        self._subscribe_to_change_font(dependencies)
        self._subscribe_to_change_text(dependencies)
        self._subscribe_to_change_move(dependencies)
        self._subscribe_to_change_color(dependencies)
        self._subscribe_to_change_dimension(dependencies)

    @property
    def text_id(self):
        return self._text_id

    @property
    def note_id(self):
        return self._note_id

    def adjust_font(self, dependencies: internal.view.dependencies.Dependencies, larger=True):
        SIZE_MULTIPLIER = 1.05

        width = int(dependencies.canvas.itemcget(self.text_id, 'width'))
        obj: internal.objects.interfaces.IBoardObjectCard = dependencies.repo.get(self.id)
        _, y1, _, y2 = dependencies.canvas.bbox(self.text_id)
        floated_size = float(obj.font.size)
        if larger:
            while abs(y1 - y2) > width:
                floated_size /= SIZE_MULTIPLIER
                font = self.get_font(dependencies)
                font.size = floated_size
                dependencies.controller.edit_font(self.id, font)
                _, y1, _, y2 = dependencies.canvas.bbox(self.text_id)
                y1 = dependencies.canvas.canvasx(y1)
                y2 = dependencies.canvas.canvasy(y2)
        else:
            increase_boundary = width * 0.7
            while abs(y1 - y2) < increase_boundary:
                floated_size *= SIZE_MULTIPLIER
                font = self.get_font(dependencies)
                font.size = floated_size
                dependencies.controller.edit_font(self.id, font)
                _, y1, _, y2 = dependencies.canvas.bbox(self.text_id)
                y1 = dependencies.canvas.canvasx(y1)
                y2 = dependencies.canvas.canvasy(y2)

    def update_coord_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectCard = dependencies.repo.get(self.id)
        x = obj.position.x
        y = obj.position.y
        width, height = obj.dimension
        dependencies.canvas.coords(self.note_id, x, y, x + width, y + height)
        dependencies.canvas.coords(self.text_id, x + width / 2, y + height / 2)
        dependencies.canvas.itemconfigure(self.text_id, width=width)

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

    def _subscribe_to_change_color(self, dependencies: internal.view.dependencies.Dependencies):
        dependencies.pub_sub_broker.subscribe(
            VIEW_OBJECT_ID,
            self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_COLOR,
            lambda publisher, event, repo: self.get_color_update_from_repo(dependencies),
        )

    def _subscribe_to_change_dimension(self, dependencies: internal.view.dependencies.Dependencies):
        dependencies.pub_sub_broker.subscribe(
            VIEW_OBJECT_ID,
            self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_DIMENSION,
            lambda publisher, event, repo: self.get_dimension_update_from_repo(dependencies),
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
                get_font_colors(),
                _FONT_COLOR_DESC,
                self.get_font_color,
                self.set_font_color,
            ),
            lambda dependencies: self._base_widget(
                dependencies,
                get_font_colors(),
                _CARD_COLOR_DESC,
                self.get_card_color,
                self.set_card_color,
            ),
            lambda dependencies: self._base_widget(
                dependencies,
                get_card_sizes(),
                _CARD_COLOR_DESC,
                self.get_card_dimension,
                self.set_card_dimension,
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

    def move_to(self, dependencies: internal.view.dependencies.Dependencies, x: int, y: int):
        self.update_coord_from_repo(dependencies)

    def get_font_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectCard = dependencies.repo.get(self.id)
        font = obj.font
        tk_font = as_tkinter_object_font(font)
        dependencies.canvas.itemconfigure(self.text_id, font=tk_font)
        dependencies.canvas.itemconfigure(self.text_id, fill=font.color)

    def get_text_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectCard = dependencies.repo.get(self.id)
        dependencies.canvas.itemconfigure(self.text_id, text=obj.text)
        self.adjust_font(dependencies)

    def get_move_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectCard = dependencies.repo.get(self.id)
        self.move_to(dependencies, obj.position.x, obj.position.y)

    def get_color_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectCard = dependencies.repo.get(self.id)
        dependencies.canvas.itemconfigure(self.note_id, fill=obj.color)

    def get_dimension_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        self.update_coord_from_repo(dependencies)

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

    def get_card_color(self, dependencies: internal.view.dependencies.Dependencies):
        return dependencies.canvas.itemcget(self.note_id, 'fill')

    def set_card_color(self, dependencies: internal.view.dependencies.Dependencies, color: str):
        dependencies.controller.edit_color(self.id, color=color)

    def get_card_dimension(self, dependencies: internal.view.dependencies.Dependencies):
        x1, y1, x2, y2 = dependencies.canvas.coords(self.note_id)
        if abs(y2 - y1) <= 150:
            return 'Small'
        elif abs(y2 - y1) <= 250:
            return 'Medium'
        else:
            """Large"""

    def set_card_dimension(
        self, dependencies: internal.view.dependencies.Dependencies, size_type: str
    ):
        if size_type == 'Small':
            dependencies.controller.edit_dimension(
                self.id, dimension=[_DEFAULT_SMALL_SIZE, _DEFAULT_SMALL_SIZE]
            )
        elif size_type == 'Medium':
            dependencies.controller.edit_dimension(
                self.id, dimension=[_DEFAULT_MEDIUM_SIZE, _DEFAULT_MEDIUM_SIZE]
            )
        else:
            dependencies.controller.edit_dimension(
                self.id, dimension=[_DEFAULT_LARGE_SIZE, _DEFAULT_LARGE_SIZE]
            )
