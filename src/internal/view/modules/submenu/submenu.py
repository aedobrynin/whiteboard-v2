import tkinter
from tkinter import ttk, Menu
from typing import List

import internal.objects.events
import internal.objects.interfaces
import internal.pub_sub.interfaces
import internal.repositories.interfaces
import internal.view.dependencies
import internal.view.modules.connector
import internal.view.modules.text
import internal.view.modules.pen
import internal.view.utils

_SUBMENU_PREFIX = 'submenu'
_BRING_TO_FRONT_DESC = 'Bring To Front'
_SEND_TO_BACK_DESC = 'Send To Back'
_DELETE_DESC = 'Delete'


class Submenu:
    obj_id: internal.objects.interfaces.ObjectId
    _property_widgets: List[ttk.Widget]
    _option_menu: Menu

    def __init__(self, obj_id: str, dependencies: internal.view.dependencies.Dependencies):
        self.obj_id = obj_id
        self._property_widgets: List[ttk.Widget] = []
        self._option_menu: Menu = None
        obj: internal.objects.interfaces.IBoardObjectWithPosition = dependencies.repo.get(obj_id)
        if obj.type in [
            internal.objects.types.BoardObjectType.TEXT,
            internal.objects.types.BoardObjectType.PEN,
            internal.objects.types.BoardObjectType.CONNECTOR
        ]:
            obj_canvas: internal.view.modules.text.TextObject = (
                dependencies.objects_storage.get_by_id(obj_id)
            )
            self._property_widgets = obj_canvas.widgets(dependencies)
        else:
            self._property_widgets = []
        self._init_option_menu(dependencies)
        self._subscribe_draw_border(dependencies)

    def _subscribe_draw_border(self, dependencies: internal.view.dependencies.Dependencies):
        dependencies.pub_sub_broker.subscribe(
            _SUBMENU_PREFIX + self.obj_id,
            self.obj_id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_SIZE,
            lambda *_: self._draw_border(dependencies),
        )

    def _draw_border(self, dependencies: internal.view.dependencies.Dependencies):
        obj = dependencies.objects_storage.get_opt_by_id(self.obj_id)
        if obj and obj.get_focused(dependencies):
            obj.draw_object_border(dependencies)

    def _remove_border(self, dependencies: internal.view.dependencies.Dependencies):
        obj = dependencies.objects_storage.get_opt_by_id(self.obj_id)
        if obj:
            obj.remove_object_border(dependencies)
            obj.set_focused(dependencies, False)

    def _init_option_menu(self, dependencies: internal.view.dependencies.Dependencies):
        self._option_menu = Menu(None, tearoff=0)
        self._option_menu.add_command(
            label=_BRING_TO_FRONT_DESC, command=lambda: self._bring_to_front(dependencies)
        )
        self._option_menu.add_command(
            label=_SEND_TO_BACK_DESC, command=lambda: self._send_to_back(dependencies)
        )
        self._option_menu.add_command(
            label=_DELETE_DESC, command=lambda: self._delete(dependencies)
        )

    def _bring_to_front(self, dependencies: internal.view.dependencies.Dependencies):
        # TODO: issue #32
        dependencies.canvas.tag_raise(self.obj_id)

    def _send_to_back(self, dependencies: internal.view.dependencies.Dependencies):
        # TODO: issue #32
        dependencies.canvas.tag_lower(self.obj_id)

    def _delete(self, dependencies: internal.view.dependencies.Dependencies):
        self.destroy_menu(dependencies)
        dependencies.controller.delete_object(self.obj_id)
        self.obj_id = None
        # to trigger predicate_from_context_to_root
        # TODO: solution without event-generate
        dependencies.canvas.event_generate('<ButtonRelease-1>')

    def show_option_menu(
        self, dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event
    ):
        self._option_menu.tk_popup(event.x_root, event.y_root, 0)

    def show_menu(self, dependencies: internal.view.dependencies.Dependencies):
        obj = dependencies.objects_storage.get_opt_by_id(self.obj_id)
        if obj:
            obj.set_focused(dependencies, True)
            self._draw_border(dependencies)
        for w in self._property_widgets:
            w.pack(pady=1, fill='both')

    def destroy_menu(self, dependencies: internal.view.dependencies.Dependencies):
        obj = dependencies.objects_storage.get_opt_by_id(self.obj_id)
        if obj:
            obj.set_focused(dependencies, False)
            self._remove_border(dependencies)
        self._option_menu.destroy()
        for w in self._property_widgets:
            w.destroy()
