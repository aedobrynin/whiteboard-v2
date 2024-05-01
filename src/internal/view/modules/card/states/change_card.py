from __future__ import annotations
from typing import Dict, Optional
import tkinter

import internal.objects.interfaces
import internal.view.dependencies
import internal.view.state_machine.interfaces
from internal.view.utils import get_current, get_current_opt
from internal.view.state_machine.impl import State
from ..view import CARD_TEXT_PREFIX

CHANGE_CARD_TEXT_STATE_NAME = 'CHANGE_CARD_TEXT'
OBJ_ID = 'obj_id'
CARD_TEXT_ID = 'text_id'


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    obj = get_current(global_dependencies)
    state_ctx[OBJ_ID]: str = obj.id
    state_ctx[CARD_TEXT_ID]: str = CARD_TEXT_PREFIX + obj.id
    global_dependencies.canvas.focus('')
    global_dependencies.canvas.focus_set()
    bbox = global_dependencies.canvas.bbox(state_ctx[CARD_TEXT_ID])
    global_dependencies.canvas.icursor(state_ctx[CARD_TEXT_ID], f'@{bbox[2]},{bbox[3]}')
    global_dependencies.canvas.focus(state_ctx[CARD_TEXT_ID])


def _handle_event(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    if event.type != tkinter.EventType.Key:
        return

    if event.keysym == 'Right':
        new_index = global_dependencies.canvas.index(state_ctx[CARD_TEXT_ID], 'insert') + 1
        global_dependencies.canvas.icursor(state_ctx[CARD_TEXT_ID], new_index)
        global_dependencies.canvas.select_clear()
        return

    if event.keysym == 'Left':
        new_index = global_dependencies.canvas.index(state_ctx[CARD_TEXT_ID], 'insert') - 1
        global_dependencies.canvas.icursor(state_ctx[CARD_TEXT_ID], new_index)
        global_dependencies.canvas.select_clear()
        return

    if event.keysym == 'BackSpace':
        insert = global_dependencies.canvas.index(state_ctx[CARD_TEXT_ID], 'insert')
        if insert > 0:
            global_dependencies.canvas.dchars(state_ctx[CARD_TEXT_ID], insert - 1, insert - 1)
        return

    # TODO: issue #12
    if event.char == '':
        return
    global_dependencies.canvas.index(state_ctx[CARD_TEXT_ID], 'insert')
    global_dependencies.canvas.insert(state_ctx[CARD_TEXT_ID], 'insert', event.char)


def _on_leave(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    global_dependencies.canvas.focus('')
    text_new: str = global_dependencies.canvas.itemcget(state_ctx[CARD_TEXT_ID], 'text')
    global_dependencies.controller.edit_text(
        state_ctx[OBJ_ID],
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
    return isinstance(cur_obj, internal.objects.interfaces.IBoardObjectCard)


def _predicate_from_edit_text_to_root(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event  # noqa
) -> bool:
    # Release Left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(
    state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
    state = State(CHANGE_CARD_TEXT_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.OBJECT_FOCUS_STATE_NAME,
        CHANGE_CARD_TEXT_STATE_NAME,
        _predicate_from_focus_to_edit_text
    )
    state_machine.add_transition(
        CHANGE_CARD_TEXT_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_edit_text_to_root
    )
    return state
