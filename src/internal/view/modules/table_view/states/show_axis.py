from __future__ import annotations
from typing import Dict
import tkinter

import internal.objects
import internal.models.position
from internal.view.state_machine.impl import State
import internal.view.state_machine.interfaces
import internal.view.dependencies
from internal.models import Position
from ..toplevel import Window
from ..view import show_axis, draw_table, get_attr_from_position

SHOW_TABLE_MENU_ENTRY_NAME = 'pivot table'
CHOSE_AXIS_STATE_NAME = 'SHOW_TABLE'
_WINDOW = 'window_add'
_TABLE = 'table_window'
_NAME = 'name'
_INITIAL_POSITION = 'obj_position'
_LAST_DRAG_EVENT_X = 'last_drag_event_x'
_LAST_DRAG_EVENT_Y = 'last_drag_event_y'
_FIRST_DRAG_EVENT_X = 'first_drag_event_x'
_FIRST_DRAG_EVENT_Y = 'first_drag_event_y'
_OBJ_ID = 'obj_id'
_MOVE_STARTED = 'moving'
_X_LIST = 'x_list'
_Y_LIST = 'y_list'
_X_OPTIONS = 'x_options'
_Y_OPTIONS = 'y_options'
_WIDTH = 'width'
_HEIGHT = 'height'


def _predicate_from_root_to_add_attribute(
        global_dependencies: internal.view.dependencies.Dependencies,
        event: tkinter.Event
) -> bool:
    if global_dependencies.menu.current_state != SHOW_TABLE_MENU_ENTRY_NAME:
        return False
    return True


def _on_enter(
        global_dependencies: internal.view.dependencies.Dependencies,
        state_ctx: Dict,
        _: tkinter.Event
):
    state_ctx[_WINDOW] = show_axis(global_dependencies)
    state_ctx[_MOVE_STARTED] = False
    global_dependencies.menu.set_selected_state()

def _handle_event(
        global_dependencies: internal.view.dependencies.Dependencies,
        state_ctx: Dict,
        event: tkinter.Event
):
    window: Window = state_ctx[_WINDOW]
    if event.type == tkinter.EventType.Deactivate and window and window.saved:
        table, x_list, x_options, y_list, y_options, width, height = draw_table(global_dependencies, window.get_vals())
        table.canvas.bind('<B1-Motion>', lambda event: move_obj_start(state_ctx, event, state_ctx[_TABLE]))
        table.canvas.bind('<ButtonRelease-1>', lambda event: moving_stop(global_dependencies, state_ctx, event, state_ctx[_TABLE]))
        state_ctx[_TABLE] = table
        state_ctx[_X_LIST] = x_list
        state_ctx[_Y_LIST] = y_list
        state_ctx[_X_OPTIONS] = x_options
        state_ctx[_Y_OPTIONS] = y_options
        state_ctx[_WIDTH] = width
        state_ctx[_HEIGHT] = height

    return


def move_obj_start(
        state_ctx: Dict,
        event: tkinter.Event,
        window: Window
):
    if state_ctx[_MOVE_STARTED]:
        x = int(window.canvas.canvasx(event.x))
        y = int(window.canvas.canvasy(event.y))
        window.canvas.move(
            state_ctx[_OBJ_ID],
            x - state_ctx[_LAST_DRAG_EVENT_X],
            y - state_ctx[_LAST_DRAG_EVENT_Y]
        )
        state_ctx[_LAST_DRAG_EVENT_X] = x
        state_ctx[_LAST_DRAG_EVENT_Y] = y
        return

    tags = window.canvas.gettags('current')
    if not tags:
        return
    state_ctx[_MOVE_STARTED] = True
    window.canvas.scan_mark(event.x, event.y)

    x = int(window.canvas.canvasx(event.x))
    y = int(window.canvas.canvasy(event.y))

    state_ctx[_LAST_DRAG_EVENT_X] = x
    state_ctx[_LAST_DRAG_EVENT_Y] = y

    state_ctx[_FIRST_DRAG_EVENT_X] = x
    state_ctx[_FIRST_DRAG_EVENT_Y] = y
    state_ctx[_INITIAL_POSITION] = Position(x, y, 1)
    state_ctx[_OBJ_ID] = tags[0]


def moving_stop(
        global_dependencies: internal.view.dependencies.Dependencies,
        state_ctx: Dict,
        _: tkinter.Event,
        window: Window
):
    if not state_ctx[_MOVE_STARTED]:
        return
    state_ctx[_MOVE_STARTED] = False
    diff: Position = Position(
        state_ctx[_LAST_DRAG_EVENT_X] - state_ctx[_FIRST_DRAG_EVENT_X],
        state_ctx[_LAST_DRAG_EVENT_Y] - state_ctx[_FIRST_DRAG_EVENT_Y],
        0
    )
    position = state_ctx[_INITIAL_POSITION] + diff

    attributes = get_attr_from_position(position, state_ctx[_X_LIST], state_ctx[_X_OPTIONS], state_ctx[_Y_LIST],
                                        state_ctx[_Y_OPTIONS], state_ctx[_WIDTH], state_ctx[_HEIGHT])
    for name, value in attributes.items():
        global_dependencies.controller.edit_attribute(state_ctx[_OBJ_ID], name, value)
    window.canvas.configure(background='white')


def _predicate_from_add_attribute_to_root(
        global_dependencies: internal.view.dependencies.Dependencies,
        event: tkinter.Event
) -> bool:
    if event.type != tkinter.EventType.Property:
        return False
    return True


def create_state(
        state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
    state = State(CHOSE_AXIS_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        CHOSE_AXIS_STATE_NAME,
        _predicate_from_root_to_add_attribute
    )
    state_machine.add_transition(
        CHOSE_AXIS_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_add_attribute_to_root
    )

    return state
