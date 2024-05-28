from __future__ import annotations

import internal.view.dependencies
from .states import add_attribute_state, show_axis_state
from .pivot_table_view import open_window as open_window


def create_states(dependencies: internal.view.dependencies):
    dependencies.state_machine.add_state(add_attribute_state.create_state(dependencies.state_machine))
    dependencies.state_machine.add_state(show_axis_state.create_state(dependencies.state_machine))


def register_module_menu(dependencies: internal.view.dependencies):
    dependencies.menu.add_command_to_menu(add_attribute_state.ADD_ATTR_MENU_ENTRY_NAME)
    dependencies.menu.add_command_to_menu(show_axis_state.SHOW_TABLE_MENU_ENTRY_NAME)


@internal.view.modules.modules.register_module('pivot_table')
def init_module(dependencies: internal.view.dependencies):
    create_states(dependencies)
    register_module_menu(dependencies)
