from __future__ import annotations
from typing import Dict, Optional
import tkinter

import internal.objects.interfaces
import internal.view.dependencies
import internal.view.state_machine.interfaces
<<<<<<< HEAD
from internal.view.utils import get_current, get_current_opt
from internal.view.state_machine.impl import State
from ..view import TEXT_PREFIX

CHANGE_TEXT_STATE_NAME = 'CHANGE_TEXT'
OBJ_ID = 'obj_id'
TEXT_ID = 'text_id'
=======
from internal.view.objects.interfaces import IViewObject
from internal.view.state_machine.impl import State
from ..consts import OBJ_ID, TEXT_CHANGE_STATE_NAME
from ..text_view import TextObject
>>>>>>> main


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
<<<<<<< HEAD
    obj = get_current(global_dependencies)
    state_ctx[OBJ_ID]: str = obj.id
    state_ctx[TEXT_ID]: str = TEXT_PREFIX + obj.id
    global_dependencies.canvas.focus('')
    global_dependencies.canvas.focus_set()
    bbox = global_dependencies.canvas.bbox(state_ctx[TEXT_ID])
    global_dependencies.canvas.icursor(state_ctx[TEXT_ID], f'@{bbox[2]},{bbox[3]}')
    global_dependencies.canvas.focus(state_ctx[TEXT_ID])
=======
    obj: TextObject = global_dependencies.objects_storage.get_current(global_dependencies)
    state_ctx[OBJ_ID]: str = obj.id
    global_dependencies.canvas.focus('')
    global_dependencies.canvas.focus_set()
    bbox = global_dependencies.canvas.bbox(obj.text_id)
    global_dependencies.canvas.icursor(obj.text_id, f'@{bbox[2]},{bbox[3]}')
    global_dependencies.canvas.focus(obj.text_id)
>>>>>>> main


def _handle_event(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    if event.type != tkinter.EventType.Key:
        return

<<<<<<< HEAD
    if event.keysym == 'Right':
        new_index = global_dependencies.canvas.index(state_ctx[TEXT_ID], 'insert') + 1
        global_dependencies.canvas.icursor(state_ctx[TEXT_ID], new_index)
=======
    obj: TextObject = global_dependencies.objects_storage.get_opt_by_id(state_ctx[OBJ_ID])
    if not obj:
        return
    if event.keysym == 'Right':
        new_index = global_dependencies.canvas.index(obj.text_id, 'insert') + 1
        global_dependencies.canvas.icursor(obj.text_id, new_index)
>>>>>>> main
        global_dependencies.canvas.select_clear()
        return

    if event.keysym == 'Left':
<<<<<<< HEAD
        new_index = global_dependencies.canvas.index(state_ctx[TEXT_ID], 'insert') - 1
        global_dependencies.canvas.icursor(state_ctx[TEXT_ID], new_index)
=======
        new_index = global_dependencies.canvas.index(obj.text_id, 'insert') - 1
        global_dependencies.canvas.icursor(obj.text_id, new_index)
>>>>>>> main
        global_dependencies.canvas.select_clear()
        return

    if event.keysym == 'BackSpace':
<<<<<<< HEAD
        insert = global_dependencies.canvas.index(state_ctx[TEXT_ID], 'insert')
        if insert > 0:
            global_dependencies.canvas.dchars(state_ctx[TEXT_ID], insert - 1, insert - 1)
        return

    # TODO: issue #12
    if event.char == '':
        return
    global_dependencies.canvas.index(state_ctx[TEXT_ID], 'insert')
    global_dependencies.canvas.insert(state_ctx[TEXT_ID], 'insert', event.char)
=======
        index = global_dependencies.canvas.index(obj.text_id, 'insert')
        if index > 0:
            text: str = global_dependencies.canvas.itemcget(obj.id, 'text')
            global_dependencies.controller.edit_text(
                state_ctx[OBJ_ID],
                text[:index - 1] + text[index:]
            )
            global_dependencies.canvas.icursor(obj.text_id, index - 1)
        return

    if event.char == '':
        return
    global_dependencies.canvas.index(obj.text_id, 'insert')
    # TODO: to many events
    index = global_dependencies.canvas.index(obj.text_id, 'insert')
    text: str = global_dependencies.canvas.itemcget(obj.id, 'text')
    global_dependencies.controller.edit_text(
        state_ctx[OBJ_ID],
        text[:index] + event.char + text[index:]
    )
    global_dependencies.canvas.icursor(obj.text_id, index + 1)
>>>>>>> main


def _on_leave(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    global_dependencies.canvas.focus('')
<<<<<<< HEAD
    text_new: str = global_dependencies.canvas.itemcget(state_ctx[TEXT_ID], 'text')
    global_dependencies.controller.edit_text(
        state_ctx[OBJ_ID],
        text_new
    )
=======
>>>>>>> main


def _predicate_from_focus_to_edit_text(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event
) -> bool:
    # Release Left mouse button
    if event.type != tkinter.EventType.ButtonRelease or event.num != 1:
        return False
<<<<<<< HEAD
    cur_obj: Optional[internal.objects.interfaces.IBoardObjectWithPosition] = get_current_opt(
        global_dependencies)
    if cur_obj is None:
        return False
    if not cur_obj.focus:
        return False
    return isinstance(cur_obj, internal.objects.interfaces.IBoardObjectText)
=======
    cur_obj: Optional[IViewObject] = global_dependencies.objects_storage.get_current_opt(
        global_dependencies
    )
    if cur_obj is None:
        return False
    if not cur_obj.get_focused(global_dependencies):
        return False
    return isinstance(cur_obj, TextObject)
>>>>>>> main


def _predicate_from_edit_text_to_root(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event  # noqa
) -> bool:
    # Release Left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(
    state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
<<<<<<< HEAD
    state = State(CHANGE_TEXT_STATE_NAME)
=======
    state = State(TEXT_CHANGE_STATE_NAME)
>>>>>>> main
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.OBJECT_FOCUS_STATE_NAME,
<<<<<<< HEAD
        CHANGE_TEXT_STATE_NAME,
        _predicate_from_focus_to_edit_text
    )
    state_machine.add_transition(
        CHANGE_TEXT_STATE_NAME,
=======
        TEXT_CHANGE_STATE_NAME,
        _predicate_from_focus_to_edit_text
    )
    state_machine.add_transition(
        TEXT_CHANGE_STATE_NAME,
>>>>>>> main
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_edit_text_to_root
    )
    return state
