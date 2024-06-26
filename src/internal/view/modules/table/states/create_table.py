from __future__ import annotations
from typing import Dict
import tkinter

import internal.objects
import internal.models.position
import internal.view.state_machine.interfaces
import internal.view.dependencies
from internal.view.state_machine.impl import State
from ..consts import TABLE_MENU_ENTRY_NAME, CREATE_TABLE_STATE_NAME


def _predicate_from_root_to_create_table(
    global_dependencies: internal.view.dependencies.Dependencies,
    event: tkinter.Event
) -> bool:
    # Press Left mouse button with text menu state
    if event.type != tkinter.EventType.ButtonPress:
        return False
    if event.num != 1:
        return False
    return global_dependencies.menu.current_state == TABLE_MENU_ENTRY_NAME


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    actual_x = global_dependencies.canvas.canvasx(event.x)
    actual_y = global_dependencies.canvas.canvasy(event.y)

    global_dependencies.controller.create_object(
        internal.objects.BoardObjectType.TABLE,
        position=internal.models.position.Position(actual_x, actual_y, z=1)
    )


def _on_leave(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    global_dependencies.menu.set_selected_state()


def _predicate_from_create_table_to_root(
    global_dependencies: internal.view.dependencies.Dependencies,
    event: tkinter.Event
) -> bool:
    # Release left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(
    state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
    state = State(CREATE_TABLE_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        CREATE_TABLE_STATE_NAME,
        _predicate_from_root_to_create_table
    )
    state_machine.add_transition(
        CREATE_TABLE_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_create_table_to_root
    )
    return state
