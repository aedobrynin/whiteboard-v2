from __future__ import annotations
from typing import Dict, Optional
import tkinter

import internal.objects.interfaces
import internal.view.dependencies
import internal.view.state_machine.interfaces
from internal.view.objects.interfaces import IViewObject
from internal.view.state_machine.impl import State
from ..consts import OBJ_ID, CARD_CHANGE_STATE_NAME
from ..card_view import CardObject


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    obj: CardObject = global_dependencies.objects_storage.get_current(global_dependencies)
    state_ctx[OBJ_ID]: str = obj.id
    global_dependencies.canvas.focus('')
    global_dependencies.canvas.focus_set()
    bbox = global_dependencies.canvas.bbox(obj.text_id)
    global_dependencies.canvas.icursor(obj.text_id, f'@{bbox[2]},{bbox[3]}')
    global_dependencies.canvas.focus(obj.text_id)


def _handle_event(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    if event.type != tkinter.EventType.Key:
        return

    obj: CardObject = global_dependencies.objects_storage.get_opt_by_id(state_ctx[OBJ_ID])
    if not obj:
        return
    if event.keysym == 'Right':
        new_index = global_dependencies.canvas.index(obj.text_id, 'insert') + 1
        global_dependencies.canvas.icursor(obj.text_id, new_index)
        global_dependencies.canvas.select_clear()
        return

    if event.keysym == 'Left':
        new_index = global_dependencies.canvas.index(obj.text_id, 'insert') - 1
        global_dependencies.canvas.icursor(obj.text_id, new_index)
        global_dependencies.canvas.select_clear()
        return

    if event.keysym == 'BackSpace':
        index = global_dependencies.canvas.index(obj.text_id, 'insert')
        if index > 0:
            text: str = global_dependencies.canvas.itemcget(obj.text_id, 'text')
            global_dependencies.controller.edit_text(
                state_ctx[OBJ_ID],
                text[:index - 1] + text[index:]
            )
            global_dependencies.canvas.icursor(obj.text_id, index - 1)
            obj.adjust_font(global_dependencies, larger=False)
        return

    if event.char == '':
        return
    global_dependencies.canvas.index(obj.text_id, 'insert')
    # TODO: to many events
    index = global_dependencies.canvas.index(obj.text_id, 'insert')
    text: str = global_dependencies.canvas.itemcget(obj.text_id, 'text')
    global_dependencies.controller.edit_text(
        state_ctx[OBJ_ID],
        text[:index] + event.char + text[index:]
    )
    global_dependencies.canvas.icursor(obj.text_id, index + 1)


def _on_leave(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    global_dependencies.canvas.focus('')


def _predicate_from_focus_to_edit_text(
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
    return isinstance(cur_obj, CardObject)


def _predicate_from_edit_text_to_root(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event  # noqa
) -> bool:
    # Release Left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(
    state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
    state = State(CARD_CHANGE_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.OBJECT_FOCUS_STATE_NAME,
        CARD_CHANGE_STATE_NAME,
        _predicate_from_focus_to_edit_text
    )
    state_machine.add_transition(
        CARD_CHANGE_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_edit_text_to_root
    )
    return state