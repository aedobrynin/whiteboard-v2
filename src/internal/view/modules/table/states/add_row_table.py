from __future__ import annotations
from typing import Dict
import tkinter

import internal.objects
import internal.objects.interfaces
import internal.models.position
from internal.view.state_machine.impl import State
import internal.view.state_machine.interfaces
import internal.view.dependencies
from ..consts import ADD_ROW_STATE_NAME
from ..table_view import TableObject


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    obj: internal.objects.interfaces.IBoardObjectTable = (
        global_dependencies.objects_storage.get_current(global_dependencies)
    )
    global_dependencies.controller.edit_table(
        obj.id, obj.columns_width, obj.rows_height + [obj.default_height]
    )


def _predicate_from_focus_to_add_row_table(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event
) -> bool:
    # Press Left mouse button with focus state
    if event.type != tkinter.EventType.ButtonPress:
        return False
    if event.num != 1:
        return False
    cur_obj = global_dependencies.objects_storage.get_current_opt(global_dependencies)
    if cur_obj is None:
        return False
    if not cur_obj.get_focused(global_dependencies):
        return False
    if not isinstance(cur_obj, TableObject):
        return False
    return cur_obj.add_row_id in global_dependencies.canvas.find_withtag('current')


def _predicate_from_add_row_to_root(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event
) -> bool:
    # Release left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(
    state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
    state = State(ADD_ROW_STATE_NAME)
    state.set_on_enter(_on_enter)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.OBJECT_FOCUS_STATE_NAME,
        ADD_ROW_STATE_NAME,
        _predicate_from_focus_to_add_row_table
    )
    state_machine.add_transition(
        ADD_ROW_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_add_row_to_root
    )
    return state
