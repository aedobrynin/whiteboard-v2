from __future__ import annotations
from typing import Dict
import tkinter

import internal.objects
import internal.models.position
from internal.view.state_machine.impl import State
import internal.view.state_machine.interfaces
import internal.view.dependencies
from ..view import open_window, get_values
ADD_ATTR_MENU_ENTRY_NAME = 'add attribute'
ADD_ATTRIBUTE_STATE_NAME = 'ADD_ATTRIBUTE'
_WINDOW = 'window_add'
_ENTRY = 'entry'
_NAME = 'name'


def _predicate_from_root_to_add_attribute(
    global_dependencies: internal.view.dependencies.Dependencies,
    event: tkinter.Event
) -> bool:
    if global_dependencies.menu.current_state != ADD_ATTR_MENU_ENTRY_NAME:
        return False

    return True

def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    _: tkinter.Event
):
    state_ctx[_WINDOW], state_ctx[_ENTRY] = open_window(global_dependencies)
    # name = get_values(state_ctx[_WINDOW], state_ctx[_ENTRY])
    # print(name)
    # if name:
    #     global_dependencies.controller.add_attribute(name)

# def _handle_event(
#     global_dependencies: internal.view.dependencies.Dependencies,
#     state_ctx: Dict,
#     event: tkinter.Event
# ):
#     name = get_values(state_ctx[_WINDOW], state_ctx[_ENTRY])
#     print(name)
#     if name:
#         global_dependencies.controller.add_attribute(name)

def _predicate_from_add_attribute_to_root(
    global_dependencies: internal.view.dependencies.Dependencies,
    event: tkinter.Event
) -> bool:
    # ВОТ ТУТ должен быть ивент выхода из конкретного окна, иначе все ломается
    if event.type != tkinter.EventType.Destroy:
        return False
    return global_dependencies.menu.current_state == ADD_ATTRIBUTE_STATE_NAME


def create_state(
    state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
    state = State(ADD_ATTRIBUTE_STATE_NAME)
    state.set_on_enter(_on_enter)
    # state.set_event_handler(_handle_event)
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
