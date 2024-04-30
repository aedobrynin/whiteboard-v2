from __future__ import annotations
from typing import Dict
import tkinter

from internal.view.state_machine.impl import State
from internal.view.utils import get_current_opt
import internal.view.state_machine.interfaces
import internal.view.dependencies

_MOVE_BOARD_STATE_NAME = 'MOVE_BOARD'


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict, # noqa
    event: tkinter.Event
):
    global_dependencies.canvas.scan_mark(event.x, event.y)


def _handle_event(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict, # noqa
    event: tkinter.Event
):
    # Motion with Left mouse button pressed
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return
    global_dependencies.canvas.scan_dragto(event.x, event.y, gain=1)


def _predicate_from_root_to_move_board(
    global_dependencies: internal.view.dependencies.Dependencies,
    event: tkinter.Event
) -> bool:
    # Motion with Left mouse button pressed
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return False
    cur_obj = get_current_opt(global_dependencies)
    return cur_obj is None


def _predicate_from_move_board_to_root(
    global_dependencies: internal.view.dependencies.Dependencies, # noqa
    event: tkinter.Event
) -> bool:
    # Release Left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(state_machine: internal.view.state_machine.interfaces.IStateMachine) -> State:
    state = State(_MOVE_BOARD_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _MOVE_BOARD_STATE_NAME,
        _predicate_from_root_to_move_board
    )
    state_machine.add_transition(
        _MOVE_BOARD_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_move_board_to_root
    )
    return state
