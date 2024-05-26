from __future__ import annotations

import logging
from typing import Dict, Optional
import tkinter

import internal.objects.interfaces
import internal.view.dependencies
import internal.view.state_machine.interfaces
from internal.view.objects.interfaces import IViewObject
from internal.view.state_machine.impl import State
from ..consts import OBJ_ID, CODE_CHANGE_STATE_NAME
from ..code_view import CodeObject


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    cur_obj: CodeObject = global_dependencies.objects_storage.get_current(global_dependencies)
    state_ctx[OBJ_ID] = cur_obj.id
    global_dependencies.canvas.tag_lower(cur_obj.rectangle_id, cur_obj.window_id)
    cur_obj.text.focus_set()


def _handle_event(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    pass


def _on_leave(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    cur_obj: Optional[CodeObject] = global_dependencies.objects_storage.get_opt_by_id(
        state_ctx[OBJ_ID]
    )
    if not cur_obj:
        logging.warning('object not found')
        return
    global_dependencies.canvas.focus('')
    global_dependencies.canvas.tag_lower(cur_obj.rectangle_id, cur_obj.window_id)


def _predicate_from_focus_to_code_text(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event
) -> bool:
    # Release Left mouse button
    if event.type != tkinter.EventType.ButtonRelease or event.num != 1:
        return False
    cur_obj: Optional[IViewObject] = global_dependencies.objects_storage.get_current_opt(
        global_dependencies
    )
    if cur_obj is None:
        return False
    if not cur_obj.get_focused(global_dependencies):
        return False
    return isinstance(cur_obj, CodeObject)


def _predicate_from_edit_code_to_root(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event  # noqa
) -> bool:
    # Release Left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(
    state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
    state = State(CODE_CHANGE_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.OBJECT_FOCUS_STATE_NAME,
        CODE_CHANGE_STATE_NAME,
        _predicate_from_focus_to_code_text
    )
    state_machine.add_transition(
        CODE_CHANGE_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_edit_code_to_root
    )
    return state
