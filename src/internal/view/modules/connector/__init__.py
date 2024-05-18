from __future__ import annotations

import internal.objects.types
import internal.view.dependencies
import internal.view.modules.modules
from .connector_view import ConnectorObject
from .consts import CONNECTOR_MODULE_NAME, CONNECTOR_MENU_ENTRY_NAME
from .states import create_connector


def create_states(dependencies: internal.view.dependencies):
    dependencies.state_machine.add_state(create_connector.create_state(dependencies.state_machine))


def register_object_types(dependencies: internal.view.dependencies):
    dependencies.objects_storage.register_object_type(
        internal.objects.types.BoardObjectType.CONNECTOR,
        ConnectorObject
    )


def register_module_menu(dependencies: internal.view.dependencies):
    dependencies.menu.add_command_to_menu(CONNECTOR_MENU_ENTRY_NAME)


@internal.view.modules.modules.register_module(CONNECTOR_MODULE_NAME)
def init_module(dependencies: internal.view.dependencies):
    create_states(dependencies)
    register_object_types(dependencies)
    register_module_menu(dependencies)
