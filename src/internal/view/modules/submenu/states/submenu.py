from __future__ import annotations

import tkinter.ttk
from typing import Dict
import tkinter

import internal.models.position
import internal.objects
import internal.objects.interfaces
import internal.view.state_machine.interfaces
import internal.view.dependencies

from internal.view.state_machine.impl import State
from internal.view.modules.submenu.submenu import Submenu

SUBMENU = 'SUBMENU'


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    obj = global_dependencies.objects_storage.get_current_opt(global_dependencies)
    if not obj:
        # TODO: log
        return
    state_ctx[SUBMENU] = Submenu(obj.id, global_dependencies)
    state_ctx[SUBMENU].show_menu(global_dependencies)


def _handle_event(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    if event.type != tkinter.EventType.ButtonRelease or event.num != 3:
        return
    submenu: Submenu = state_ctx[SUBMENU]
    submenu.show_option_menu(global_dependencies, event)


def _on_leave(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    if SUBMENU not in state_ctx:
        return
    submenu: Submenu = state_ctx[SUBMENU]
    if submenu.obj_id is not None:
        state_ctx[SUBMENU].destroy_menu(global_dependencies)


def _predicate_from_root_to_context(
    global_dependencies: internal.view.dependencies.Dependencies,
    event: tkinter.Event
) -> bool:
    # Release Left mouse button
    if event.type != tkinter.EventType.ButtonRelease or event.num != 1:
        return False
    cur_obj = global_dependencies.objects_storage.get_current_opt(global_dependencies)
    return cur_obj is not None


def _predicate_from_context_to_root(
    global_dependencies: internal.view.dependencies.Dependencies,
    event: tkinter.Event
) -> bool:
    # Release Left mouse button
    if event.type != tkinter.EventType.ButtonRelease or event.num != 1:
        return False
    cur_obj = global_dependencies.objects_storage.get_current_opt(global_dependencies)
    return cur_obj is None


def _predicate_from_context_to_context(
    global_dependencies: internal.view.dependencies.Dependencies,
    event: tkinter.Event
) -> bool:
    # Release Left mouse button
    if event.type != tkinter.EventType.ButtonRelease or event.num != 1:
        return False
    cur_obj = global_dependencies.objects_storage.get_current_opt(global_dependencies)
    return cur_obj is not None


def create_state(
    state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
    state = State(
        internal.view.state_machine.interfaces.OBJECT_FOCUS_STATE_NAME
    )
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        internal.view.state_machine.interfaces.OBJECT_FOCUS_STATE_NAME,
        _predicate_from_root_to_context,
    )
    state_machine.add_transition(
        internal.view.state_machine.interfaces.OBJECT_FOCUS_STATE_NAME,
        internal.view.state_machine.interfaces.OBJECT_FOCUS_STATE_NAME,
        _predicate_from_context_to_context,
    )
    state_machine.add_transition(
        internal.view.state_machine.interfaces.OBJECT_FOCUS_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_context_to_root,
    )
    return state
