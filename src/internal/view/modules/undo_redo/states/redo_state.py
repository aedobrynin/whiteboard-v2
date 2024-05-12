from __future__ import annotations
from typing import Dict
import tkinter

from internal.view.state_machine.impl import State
import internal.view.state_machine.interfaces
import internal.view.dependencies

_REDO_LAST_ACTION_STATE_NAME = 'REDO_LAST_ACTION'


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event,
):
    global_dependencies.controller.redo_last_action()


def _predicate_from_root_to_redo(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event
) -> bool:
    # Ctrl + Y
    return (
        event.type == tkinter.EventType.Key and event.keysym == 'y' and event.state & (1 << 2) > 0
    )


def _predicate_from_redo_to_root(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event
) -> bool:
    return True


def create_state(state_machine: internal.view.state_machine.interfaces.IStateMachine) -> State:
    state = State(_REDO_LAST_ACTION_STATE_NAME)
    state.set_on_enter(_on_enter)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _REDO_LAST_ACTION_STATE_NAME,
        _predicate_from_root_to_redo,
    )
    state_machine.add_transition(
        _REDO_LAST_ACTION_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_redo_to_root,
    )
    return state
