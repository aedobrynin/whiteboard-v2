from __future__ import annotations
from typing import Dict, Optional
import tkinter

import internal.objects.interfaces
import internal.view.dependencies
import internal.view.state_machine.interfaces
from internal.view.utils import get_current, get_current_opt
from internal.view.state_machine.impl import State

CHANGE_TEXT_STATE_NAME = 'CHANGE_TEXT'
TEXT = 'text'


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    obj = get_current(global_dependencies)
    state_ctx[TEXT]: internal.objects.interfaces.IBoardObjectText = obj
    global_dependencies.canvas.focus('')
    global_dependencies.canvas.focus_set()
    bbox = global_dependencies.canvas.bbox(obj.id)
    global_dependencies.canvas.icursor(obj.id, f'@{bbox[2]},{bbox[3]}')
    global_dependencies.canvas.focus(obj.id)


def _handle_event(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    if event.type != tkinter.EventType.Key:
        return

    cur_obj: internal.objects.interfaces.IBoardObjectText = state_ctx[TEXT]

    if event.keysym == 'Right':
        new_index = global_dependencies.canvas.index(cur_obj.id, 'insert') + 1
        global_dependencies.canvas.icursor(cur_obj.id, new_index)
        global_dependencies.canvas.select_clear()
        return

    if event.keysym == 'Left':
        new_index = global_dependencies.canvas.index(cur_obj.id, 'insert') - 1
        global_dependencies.canvas.icursor(cur_obj.id, new_index)
        global_dependencies.canvas.select_clear()
        return

    if event.keysym == 'BackSpace':
        insert = global_dependencies.canvas.index(cur_obj.id, 'insert')
        if insert > 0:
            global_dependencies.canvas.dchars(cur_obj.id, insert - 1, insert - 1)
        return

    # TODO: issue #12
    if event.char == '':
        return
    global_dependencies.canvas.index(cur_obj.id, 'insert')
    global_dependencies.canvas.insert(cur_obj.id, 'insert', event.char)


def _on_leave(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    global_dependencies.canvas.focus('')
    cur_obj: internal.objects.interfaces.IBoardObjectText = state_ctx[TEXT]
    text_new: str = global_dependencies.canvas.itemcget(cur_obj.id, 'text')

    global_dependencies.controller.edit_text(
        cur_obj.id,
        text_new
    )


def _predicate_from_focus_to_edit_text(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event
) -> bool:
    # Release Left mouse button
    if event.type != tkinter.EventType.ButtonRelease or event.num != 1:
        return False
    cur_obj: Optional[internal.objects.interfaces.IBoardObjectWithPosition] = get_current_opt(
        global_dependencies)
    if cur_obj is None:
        return False
    if not cur_obj.focus:
        return False
    return isinstance(cur_obj, internal.objects.interfaces.IBoardObjectText)


def _predicate_from_edit_text_to_root(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event  # noqa
) -> bool:
    # Release Left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(
    state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
    state = State(CHANGE_TEXT_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.OBJECT_FOCUS_STATE_NAME,
        CHANGE_TEXT_STATE_NAME,
        _predicate_from_focus_to_edit_text
    )
    state_machine.add_transition(
        CHANGE_TEXT_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_edit_text_to_root
    )
    return state
