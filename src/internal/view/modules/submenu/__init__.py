from __future__ import annotations
import internal.view.modules.modules
import internal.view.dependencies
from .states import submenu_state
from .consts import SUBMENU_MODULE_NAME


def create_states(dependencies: internal.view.dependencies):
    dependencies.state_machine.add_state(submenu_state.create_state(dependencies.state_machine))


@internal.view.modules.modules.register_module(SUBMENU_MODULE_NAME)
def init_module(dependencies: internal.view.dependencies):
    create_states(dependencies)
