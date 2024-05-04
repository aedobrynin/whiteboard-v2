from __future__ import annotations

import internal.view.dependencies
from .states import create_line
from .view import create_pen_object as create_pen_object


def create_states(dependencies: internal.view.dependencies):
    dependencies.state_machine.add_state(create_line.create_state(dependencies.state_machine))


def register_module_menu(dependencies: internal.view.dependencies):
    dependencies.menu.add_command_to_menu(create_line.PEN_MENU_ENTRY_NAME)


@internal.view.modules.modules.register_module('pen')
def init_module(dependencies: internal.view.dependencies):
    create_states(dependencies)
    register_module_menu(dependencies)
