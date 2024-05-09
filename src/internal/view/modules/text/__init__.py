from __future__ import annotations

import internal.objects.types
import internal.view.dependencies
from .states import create_text, change_text
from .text_view import TextObject
from .consts import TEXT_MODULE_NAME


def create_states(dependencies: internal.view.dependencies):
    dependencies.state_machine.add_state(create_text.create_state(dependencies.state_machine))
    dependencies.state_machine.add_state(change_text.create_state(dependencies.state_machine))


def register_object_types(dependencies: internal.view.dependencies):
    dependencies.objects_storage.register_object_type(
        internal.objects.types.BoardObjectType.TEXT,
        TextObject
    )


def register_module_menu(dependencies: internal.view.dependencies):
    dependencies.menu.add_command_to_menu(create_text.TEXT_MENU_ENTRY_NAME)


@internal.view.modules.modules.register_module(TEXT_MODULE_NAME)
def init_module(dependencies: internal.view.dependencies):
    create_states(dependencies)
    register_object_types(dependencies)
    register_module_menu(dependencies)
