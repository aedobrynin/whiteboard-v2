from __future__ import annotations

import internal.objects
import internal.view.dependencies
from .states import create_group
from .group_view import GroupObject
from .consts import GROUP_MENU_ENTRY_NAME, GROUP_MODULE_NAME


def create_states(dependencies: internal.view.dependencies):
    dependencies.state_machine.add_state(create_group.create_state(dependencies.state_machine))


def register_module_menu(dependencies: internal.view.dependencies):
    dependencies.menu.add_command_to_menu(GROUP_MENU_ENTRY_NAME)


def register_object_types(dependencies: internal.view.dependencies):
    dependencies.objects_storage.register_object_type(
        internal.objects.BoardObjectType.GROUP,
        GroupObject
    )


@internal.view.modules.modules.register_module(GROUP_MODULE_NAME)
def init_module(dependencies: internal.view.dependencies):
    create_states(dependencies)
    register_object_types(dependencies)
    register_module_menu(dependencies)
