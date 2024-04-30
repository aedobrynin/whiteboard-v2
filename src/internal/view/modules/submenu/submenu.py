import tkinter
from tkinter import ttk, Menu
from typing import List, Dict, Callable

import internal.objects.interfaces
import internal.view.dependencies
import internal.view.utils
from .widgets import font_color_widget


class Submenu:
    obj_id: internal.objects.interfaces.ObjectId
    _property_widgets: List[ttk.Widget]
    _option_menu: Menu
    _props: List[str]

    def __init__(
        self,
        obj_id: str,
        dependencies: internal.view.dependencies.Dependencies
    ):
        self.obj_id = obj_id
        self._property_widgets: List[ttk.Widget] = []
        self._option_menu: Menu = None
        obj: internal.objects.interfaces.IBoardObjectWithPosition = dependencies.repo.get(obj_id)
        self._props = obj.props
        for prop in self._props:
            if prop in self._prop_to_func:
                label, combobox = self._prop_to_func[prop](dependencies, obj_id)
                self._property_widgets.append(label)
                self._property_widgets.append(combobox)
        self._init_option_menu(dependencies)

    def _init_option_menu(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        self._option_menu = Menu(None, tearoff=0)
        self._option_menu.add_command(
            label='Bring To Front', command=lambda: self._bring_to_front(dependencies)
        )
        self._option_menu.add_command(
            label='Send To Back', command=lambda: self._send_to_back(dependencies))
        self._option_menu.add_command(
            label='Delete', command=lambda: self._delete(dependencies)
        )

    @property
    def _prop_to_func(self) -> Dict[str, Callable]:
        return {
            'font-color': font_color_widget
        }

    def _bring_to_front(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        dependencies.canvas.tag_raise(self.obj_id)

    def _send_to_back(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        dependencies.canvas.tag_lower(self.obj_id)

    def _delete(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
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

    def show_menu(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        internal.view.utils.draw_border(dependencies, obj_id=self.obj_id)
        dependencies.controller.edit_focus(obj_id=self.obj_id, focus=True)
        for w in self._property_widgets:
            w.pack(pady=1, fill='both')

    def destroy_menu(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        internal.view.utils.remove_border(dependencies, obj_id=self.obj_id)
        dependencies.controller.edit_focus(obj_id=self.obj_id, focus=False)
        self._option_menu.destroy()
        for w in self._property_widgets:
            w.destroy()
