from __future__ import annotations

import internal.view.modules.modules
import internal.objects.types
import internal.view.dependencies
from .states import create_line
from .pen_view import PenObject
from .consts import PEN_MENU_ENTRY_NAME, PEN_MODULE_NAME


def create_states(dependencies: internal.view.dependencies):
    dependencies.state_machine.add_state(create_line.create_state(dependencies.state_machine))


def register_object_types(dependencies: internal.view.dependencies):
    dependencies.objects_storage.register_object_type(
        internal.objects.types.BoardObjectType.PEN, PenObject
    )


def register_module_menu(dependencies: internal.view.dependencies):
    dependencies.menu.add_command_to_menu(PEN_MENU_ENTRY_NAME)


@internal.view.modules.modules.register_module(PEN_MODULE_NAME)
def init_module(dependencies: internal.view.dependencies):
    create_states(dependencies)
    register_object_types(dependencies)
    register_module_menu(dependencies)
