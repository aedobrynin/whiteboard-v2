from __future__ import annotations
import internal.view.modules.modules
import internal.objects.types
import internal.view.dependencies
from .consts import TABLE_MODULE_NAME, TABLE_MENU_ENTRY_NAME
from .states import create_table, resize_table, add_column_table, add_row_table
from .table_view import TableObject


def create_states(dependencies: internal.view.dependencies):
    dependencies.state_machine.add_state(create_table.create_state(dependencies.state_machine))
    dependencies.state_machine.add_state(resize_table.create_state(dependencies.state_machine))
    dependencies.state_machine.add_state(add_column_table.create_state(dependencies.state_machine))
    dependencies.state_machine.add_state(add_row_table.create_state(dependencies.state_machine))


def register_module_menu(dependencies: internal.view.dependencies):
    dependencies.menu.add_command_to_menu(TABLE_MENU_ENTRY_NAME)


def register_object_types(dependencies: internal.view.dependencies):
    dependencies.objects_storage.register_object_type(
        internal.objects.types.BoardObjectType.TABLE,
        TableObject
    )


@internal.view.modules.modules.register_module(TABLE_MODULE_NAME)
def init_module(dependencies: internal.view.dependencies):
    create_states(dependencies)
    register_module_menu(dependencies)
    register_object_types(dependencies)
