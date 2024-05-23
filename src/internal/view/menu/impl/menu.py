import tkinter
from typing import Callable


class Menu:
    _menu_bar: tkinter.Menu  # field to add menu items
    _current_state: str
    MENU_ROOT_STATE = 'select'

    def __init__(self, root: tkinter.Tk):
        self._menu_bar = tkinter.Menu(root)
        # by default, we add select
        self._menu_bar.add_command(
            label=self.MENU_ROOT_STATE,
            command=lambda: self.set_selected_state(self.MENU_ROOT_STATE),
        )
        self._current_state = self.MENU_ROOT_STATE
        self.set_selected_state(self.MENU_ROOT_STATE)
        root.config(menu=self._menu_bar)

    def bind(self, func: Callable):
        self._menu_bar.bind_all('<<MenuSelect>>', func)

    @property
    def current_state(self):
        return self._current_state

    def add_command_to_menu(self, name: str):
        self._menu_bar.add_command(label=name, command=lambda: self.set_selected_state(name))

    def set_selected_state(self, name: str = MENU_ROOT_STATE):
        if self._current_state == name:
            self._current_state = self.MENU_ROOT_STATE
        else:
            self._current_state = name
