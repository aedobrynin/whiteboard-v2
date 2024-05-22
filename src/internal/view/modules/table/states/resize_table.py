from __future__ import annotations
from typing import Dict
import tkinter

import internal.objects.interfaces
import internal.view.dependencies
import internal.view.state_machine.interfaces
from internal.view.modules.table.table_view import resize_column, resize_row
from internal.view.state_machine.impl import State
from ..consts import OBJ_ID, OBJ, LIST_ROW, LIST_COL, RESIZE_TABLE_STATE_NAME

_LAST_DRAG_EVENT_X = 'last_drag_event_x'
_LAST_DRAG_EVENT_Y = 'last_drag_event_y'
_AXIS = 'axis'
_COLUMN = 0
_ROW = 1
_CURRENT_COLUMN = 'current_col'
_CURRENT_ROW = 'current_row'


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    global_dependencies.canvas.scan_mark(event.x, event.y)

    x = int(global_dependencies.canvas.canvasx(event.x))
    y = int(global_dependencies.canvas.canvasy(event.y))

    obj = global_dependencies.objects_storage.get_current(global_dependencies)
    state_ctx[OBJ_ID] = obj.id

    state_ctx[OBJ]: internal.objects.interfaces.IBoardObjectTable = obj
    state_ctx[_LAST_DRAG_EVENT_X] = x
    state_ctx[_LAST_DRAG_EVENT_Y] = y
    if obj.id + 'col_l' in global_dependencies.canvas.gettags('current'):
        state_ctx[_AXIS] = _COLUMN
        c = int(global_dependencies.canvas.gettags('current')[3])
        state_ctx[_CURRENT_COLUMN] = c
    elif obj.id + 'row_l' in global_dependencies.canvas.gettags('current'):
        state_ctx[_AXIS] = _ROW
        r = int(global_dependencies.canvas.gettags('current')[3])
        state_ctx[_CURRENT_ROW] = r


def _handle_event(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    # Motion with Left mouse button pressed
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return

    x = int(global_dependencies.canvas.canvasx(event.x))
    y = int(global_dependencies.canvas.canvasy(event.y))
    obj: internal.objects.interfaces.IBoardObjectTable = state_ctx[OBJ]

    if state_ctx[_AXIS] == _COLUMN:
        c = state_ctx[_CURRENT_COLUMN]
        state_ctx[LIST_COL], state_ctx[LIST_ROW] = resize_column(global_dependencies, obj, c, x)

    if state_ctx[_AXIS] == _ROW:
        r = state_ctx[_CURRENT_ROW]
        state_ctx[LIST_COL], state_ctx[LIST_ROW] = resize_row(global_dependencies, obj, r, y)

    state_ctx[_LAST_DRAG_EVENT_X] = x
    state_ctx[_LAST_DRAG_EVENT_Y] = y


def _on_leave(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    global_dependencies.controller.edit_table(
        state_ctx[OBJ_ID], state_ctx[LIST_COL], state_ctx[LIST_ROW]
    )


def _predicate_from_focus_to_resize_table(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event
) -> bool:
    # Motion with Left mouse button pressed
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return False

    cur_obj = global_dependencies.objects_storage.get_current_opt(global_dependencies)
    if cur_obj is None:
        return False
    if not cur_obj.get_focused(global_dependencies):
        return False
    if 'line' not in global_dependencies.canvas.gettags('current'):
        return False
    return isinstance(cur_obj, internal.objects.interfaces.IBoardObjectTable)


def _predicate_from_resize_table_to_root(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event  # noqa
) -> bool:
    # Release Left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(
    state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
    state = State(RESIZE_TABLE_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.OBJECT_FOCUS_STATE_NAME,
        RESIZE_TABLE_STATE_NAME,
        _predicate_from_focus_to_resize_table
    )
    state_machine.add_transition(
        RESIZE_TABLE_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_resize_table_to_root
    )
    return state
