import tkinter
from tkinter import ttk
from typing import List, Callable

import internal.objects.interfaces
import internal.view.dependencies
import internal.view.utils
from internal.view.utils.props_values import (
    get_font_families,
    get_font_weights,
    get_font_slants,
    get_font_colors,
    get_font_sizes
)

from .view import CARD_TEXT_PREFIX, CARD_NOTE_PREFIX


def widgets(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId
) -> List[ttk.Widget]:
    _widgets = []
    for func in _widgets_func():
        label, combobox = func(dependencies, obj_id)
        _widgets.append(label)
        _widgets.append(combobox)

    card: internal.objects.interfaces.IBoardObjectCard = dependencies.repo.get(obj_id)
    for attr, value in card.attributes.items():
        label, entry = _attribute_widget(
            dependencies,
            obj_id,
            attr,
            _get_attribute,
            _set_attribute
        )
        _widgets.append(label)
        _widgets.append(entry)

    return _widgets


def _widgets_func() -> List[Callable]:
    return [
        lambda dependencies, obj_id: _base_widget(
            dependencies,
            obj_id,
            get_font_families(),
            'Шрифт',
            _get_font_family,
            _set_font_family
        ),
        lambda dependencies, obj_id: _base_widget(
            dependencies,
            obj_id,
            get_font_slants(),
            'Наклон шрифта',
            _get_font_slant,
            _set_font_slant
        ),
        lambda dependencies, obj_id: _base_widget(
            dependencies,
            obj_id,
            get_font_weights(),
            'Насыщенность шрифта',
            _get_font_weight,
            _set_font_weight
        ),
        lambda dependencies, obj_id: _base_widget(
            dependencies,
            obj_id,
            get_font_sizes(),
            'Размер шрифта',
            _get_font_size,
            _set_font_size
        ),
        lambda dependencies, obj_id: _base_widget(
            dependencies,
            obj_id,
            get_font_colors(),
            'Цвет шрифта',
            _get_color,
            _set_color
        ),
        lambda dependencies, obj_id: _base_widget(
            dependencies,
            obj_id,
            get_font_colors(),
            'Цвет карточки',
            _get_card_color,
            _set_card_color
        )
    ]


# def _attributes_widgets_func():
#     temp = []
#     for


def _base_widget(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
        restrictions: List,
        description: str,
        getter: Callable,
        setter: Callable
) -> List[ttk.Widget]:
    string_var = tkinter.StringVar()
    label = ttk.Label(
        dependencies.property_bar,
        text=description,
        justify='left',
        anchor='w'
    )
    combobox = tkinter.ttk.Combobox(
        dependencies.property_bar,
        textvariable=string_var,
        values=restrictions,
        state='readonly'
    )
    string_var.trace('w', lambda *_: setter(
        dependencies, obj_id, string_var.get()
    ))
    combobox.current(restrictions.index(getter(
        dependencies, obj_id
    )))
    return label, combobox


def _attribute_widget(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
        description: str,
        getter: Callable,
        setter: Callable
) -> List[ttk.Widget]:
    string_var = tkinter.StringVar(value=getter(dependencies, obj_id, description))
    label = ttk.Label(
        dependencies.property_bar,
        text=description,
        justify='left',
        anchor='w'
    )
    entry = tkinter.ttk.Entry(
        dependencies.property_bar,
        textvariable=string_var,
    )
    string_var.trace('w', lambda *_: setter(
        dependencies, obj_id, description, string_var.get()
    ))

    return label, entry


def _get_font(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
):
    font = dependencies.canvas.itemcget(CARD_TEXT_PREFIX + obj_id, 'font')
    font = font.split()
    font[1] = int(font[1])
    # family size weight slant
    return font


def _get_font_slant(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
):
    font = _get_font(dependencies, obj_id)
    return font[3]


def _set_font_slant(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
        value: str
):
    font = _get_font(dependencies, obj_id)
    font[3] = value
    dependencies.canvas.itemconfig(CARD_TEXT_PREFIX + obj_id, font=tuple(font))
    dependencies.controller.edit_font(obj_id, slant=font[3])


def _get_font_weight(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
):
    font = _get_font(dependencies, obj_id)
    return font[2]


def _set_font_weight(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
        value: str
):
    font = _get_font(dependencies, obj_id)
    font[2] = value
    dependencies.canvas.itemconfig(CARD_TEXT_PREFIX + obj_id, font=tuple(font))
    dependencies.controller.edit_font(obj_id, weight=font[2])


def _get_font_family(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
):
    font = _get_font(dependencies, obj_id)
    return font[0]


def _set_font_family(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
        value: str
):
    font = _get_font(dependencies, obj_id)
    font[0] = value
    dependencies.canvas.itemconfig(CARD_TEXT_PREFIX + obj_id, font=tuple(font))
    dependencies.controller.edit_font(obj_id, family=font[0])


def _get_font_size(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
):
    font = _get_font(dependencies, obj_id)
    return font[1]


def _set_font_size(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
        value: str
):
    font = _get_font(dependencies, obj_id)
    font[1] = value
    dependencies.canvas.itemconfig(CARD_TEXT_PREFIX + obj_id, font=tuple(font))
    dependencies.controller.edit_font(obj_id, size=font[1])


def _get_color(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
):
    return dependencies.canvas.itemcget(CARD_TEXT_PREFIX + obj_id, 'fill')


def _set_color(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
        color: str
):
    dependencies.canvas.itemconfig(CARD_TEXT_PREFIX + obj_id, fill=color)
    dependencies.controller.edit_font(obj_id, color=color)


def _get_card_color(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
):
    return dependencies.canvas.itemcget(CARD_NOTE_PREFIX + obj_id, 'fill')


def _set_card_color(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
        color: str
):
    dependencies.canvas.itemconfig(CARD_NOTE_PREFIX + obj_id, fill=color)
    dependencies.controller.edit_color(obj_id, color=color)


def _get_attribute(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
        attr_name: str
):
    card: internal.objects.interfaces.IBoardObjectCard = dependencies.repo.get(obj_id)
    print(card.attributes[attr_name])
    return card.attributes[attr_name]
    # return dependencies.canvas.itemcget(CARD_NOTE_PREFIX + obj_id, 'fill')


def _set_attribute(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId,
        attr_name: str,
        value: str
):
    dependencies.controller.edit_attribute(obj_id, attr_name, value)
