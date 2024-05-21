from __future__ import annotations
from typing import Dict
import tkinter

import internal.objects
import internal.models.position
<<<<<<< HEAD
from internal.view.state_machine.impl import State
import internal.view.state_machine.interfaces
import internal.view.dependencies

TEXT_MENU_ENTRY_NAME = 'text'
CREATE_TEXT_STATE_NAME = 'CREATE_TEXT'
=======
import internal.view.state_machine.interfaces
import internal.view.dependencies
from internal.view.state_machine.impl import State
from ..consts import TEXT_MENU_ENTRY_NAME, TEXT_CREATE_STATE_NAME
>>>>>>> main


def _predicate_from_root_to_create_text(
    global_dependencies: internal.view.dependencies.Dependencies,
    event: tkinter.Event
) -> bool:
    # Press Left mouse button with text menu state
    if event.type != tkinter.EventType.ButtonPress:
        return False
    if event.num != 1:
        return False
    if global_dependencies.menu.current_state != TEXT_MENU_ENTRY_NAME:
        return False

    actual_x = int(global_dependencies.canvas.canvasx(event.x))
    actual_y = int(global_dependencies.canvas.canvasy(event.y))

    global_dependencies.controller.create_object(
        internal.objects.BoardObjectType.TEXT,
<<<<<<< HEAD
        internal.models.position.Position(actual_x, actual_y, z=1)
=======
        position=internal.models.position.Position(actual_x, actual_y, z=1)
>>>>>>> main
    )
    return True


def _on_leave(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    global_dependencies.menu.set_selected_state()


def _predicate_from_create_text_to_root(
    global_dependencies: internal.view.dependencies.Dependencies,
    event: tkinter.Event
) -> bool:
    # Release left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(
    state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
<<<<<<< HEAD
    state = State(CREATE_TEXT_STATE_NAME)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        CREATE_TEXT_STATE_NAME,
        _predicate_from_root_to_create_text
    )
    state_machine.add_transition(
        CREATE_TEXT_STATE_NAME,
=======
    state = State(TEXT_CREATE_STATE_NAME)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        TEXT_CREATE_STATE_NAME,
        _predicate_from_root_to_create_text
    )
    state_machine.add_transition(
        TEXT_CREATE_STATE_NAME,
>>>>>>> main
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_create_text_to_root
    )
    return state
