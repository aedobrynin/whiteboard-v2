from __future__ import annotations
from typing import Dict
import tkinter

import internal.objects
import internal.models.position
from internal.view.state_machine.impl import State
import internal.view.state_machine.interfaces
import internal.view.dependencies
from ..toplevel import Window
from ..pivot_table_view import open_window, NAME

ADD_ATTR_MENU_ENTRY_NAME = 'add attribute'
ADD_ATTRIBUTE_STATE_NAME = 'ADD_ATTRIBUTE'
_WINDOW = 'toplevel_window'


def _predicate_from_root_to_add_attribute(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event
) -> bool:
    if global_dependencies.menu.current_state != ADD_ATTR_MENU_ENTRY_NAME:
        return False

    return True


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    state_ctx[_WINDOW] = open_window(global_dependencies)


def _on_leave(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    name: Window = state_ctx[_WINDOW]
    if name.saved:
        global_dependencies.controller.add_attribute(name.get_vals()[NAME])
    global_dependencies.menu.set_selected_state()


def _predicate_from_add_attribute_to_root(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event
) -> bool:
    if event.type != tkinter.EventType.Deactivate:
        return False

    return True


def create_state(
    state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
    state = State(ADD_ATTRIBUTE_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        ADD_ATTRIBUTE_STATE_NAME,
        _predicate_from_root_to_add_attribute
    )
    state_machine.add_transition(
        ADD_ATTRIBUTE_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_add_attribute_to_root
    )
    return state
