import internal.view.modules.modules
import internal.view.dependencies
from .states import undo_state


def create_states(dependencies: internal.view.dependencies.Dependencies):
    dependencies.state_machine.add_state(undo_state.create_state(dependencies.state_machine))


@internal.view.modules.modules.register_module('undo_redo')
def init_module(dependencies: internal.view.dependencies.Dependencies):
    create_states(dependencies)
