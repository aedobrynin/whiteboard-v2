import internal.view.dependencies
import internal.view.modules.move_object.states.move_object


def create_states(dependencies: internal.view.dependencies.Dependencies):
    dependencies.state_machine.add_state(
        internal.view.modules.move_object.states.move_object.create_state(
            dependencies.state_machine)
    )


@internal.view.modules.modules.register_module('move_object')
def init_module(dependencies: internal.view.dependencies.Dependencies):
    create_states(dependencies)
