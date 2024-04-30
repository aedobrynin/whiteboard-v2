from __future__ import annotations

import internal.view.dependencies
from .states import submenu


def create_states(dependencies: internal.view.dependencies):
    dependencies.state_machine.add_state(submenu.create_state(dependencies.state_machine))


@internal.view.modules.modules.register_module('submenu')
def init_module(dependencies: internal.view.dependencies):
    create_states(dependencies)
