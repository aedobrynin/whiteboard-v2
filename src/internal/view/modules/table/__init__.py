from __future__ import annotations

import internal.view.dependencies
from .states import create_table, resize_table, add_column_table, add_row_table, add_object
from .view import create_table_object as create_table_object


def create_states(dependencies: internal.view.dependencies):
    dependencies.state_machine.add_state(create_table.create_state(dependencies.state_machine))
    dependencies.state_machine.add_state(resize_table.create_state(dependencies.state_machine))
    dependencies.state_machine.add_state(add_column_table.create_state(dependencies.state_machine))
    dependencies.state_machine.add_state(add_row_table.create_state(dependencies.state_machine))
    dependencies.state_machine.add_state(add_object.create_state(dependencies.state_machine))


def register_module_menu(dependencies: internal.view.dependencies):
    dependencies.menu.add_command_to_menu(create_table.TABLE_MENU_ENTRY_NAME)


@internal.view.modules.modules.register_module('table')
def init_module(dependencies: internal.view.dependencies):
    create_states(dependencies)
    register_module_menu(dependencies)
