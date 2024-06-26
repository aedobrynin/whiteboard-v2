import internal.view.modules.modules
import internal.view.dependencies
from .states import drag_board_state


def create_states(dependencies: internal.view.dependencies.Dependencies):
    dependencies.state_machine.add_state(drag_board_state.create_state(dependencies.state_machine))


@internal.view.modules.modules.register_module('drag_board')
def init_module(dependencies: internal.view.dependencies.Dependencies):
    create_states(dependencies)
