from __future__ import annotations
from typing import Dict, Optional
import tkinter

import internal.objects
import internal.objects.interfaces
import internal.models.position
from internal.view.modules.table.view import add_column
from internal.view.state_machine.impl import State
import internal.view.state_machine.interfaces
from internal.view.utils import get_current, get_current_opt
import internal.view.dependencies

TABLE = 'table'
ADD_COLUMN_STATE_NAME = 'ADD_COLUMN'
_OBJ_ID = 'table_id'
_LIST_COL = 'list_col'
_LIST_ROW = 'list_row'
def _on_enter(
        global_dependencies: internal.view.dependencies.Dependencies,
        state_ctx: Dict,
        event: tkinter.Event
):
    obj = get_current(global_dependencies)
    state_ctx[TABLE] = obj
    state_ctx[_OBJ_ID] = obj.id
    state_ctx[_LIST_COL], state_ctx[_LIST_ROW] = add_column(global_dependencies, obj)

def _predicate_from_focus_to_add_column_table(
        global_dependencies: internal.view.dependencies.Dependencies,
        event: tkinter.Event
) -> bool:
    # Press Left mouse button with focus state
    if event.type != tkinter.EventType.ButtonPress:
        return False
    if event.num != 1:
        return False
    cur_obj: Optional[internal.objects.interfaces.IBoardObjectTable] = get_current_opt(
        global_dependencies)
    if cur_obj is None:
        return False
    if not cur_obj.focus:
        return False
    if cur_obj.id + 'add_c' not in global_dependencies.canvas.gettags('current'):
        return False

    return isinstance(cur_obj, internal.objects.interfaces.IBoardObjectTable)


def _on_leave(
        global_dependencies: internal.view.dependencies.Dependencies,
        state_ctx: Dict,
        __: tkinter.Event
):
    print(state_ctx[_OBJ_ID],
        state_ctx[_LIST_COL],
        state_ctx[_LIST_ROW])
    global_dependencies.controller.change_table(
        state_ctx[_OBJ_ID],
        state_ctx[_LIST_COL],
        state_ctx[_LIST_ROW]
    )


def _predicate_from_add_column_to_root(
        _: internal.view.dependencies.Dependencies,
        event: tkinter.Event
) -> bool:
    # Release left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(
        state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
    state = State(ADD_COLUMN_STATE_NAME)
    state.set_on_enter(_on_enter)

    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.OBJECT_FOCUS_STATE_NAME,
        ADD_COLUMN_STATE_NAME,
        _predicate_from_focus_to_add_column_table
    )
    state_machine.add_transition(
        ADD_COLUMN_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_add_column_to_root
    )
    return state
