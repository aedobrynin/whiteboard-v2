from __future__ import annotations

import logging
from typing import Dict
import tkinter

import internal.models
import internal.objects.interfaces
import internal.view.dependencies
import internal.view.state_machine.interfaces
from internal.view.state_machine.impl import State
from ..view import PEN_LINE_PREFIX, get_object_points

PEN_MENU_ENTRY_NAME = 'pen'
_PEN_CREATE_STATE_NAME = 'PEN_CREATE'
_OBJ_ID = 'obj_id'
_PEN_LINE_ID = 'line_id'


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    x = int(global_dependencies.canvas.canvasx(event.x))
    y = int(global_dependencies.canvas.canvasy(event.y))

    global_dependencies.controller.create_object(
        internal.objects.BoardObjectType.PEN,
        internal.models.position.Position(x, y, z=1)
    )
    # TODO: full cringe.... but i don`t have other options
    nearest = global_dependencies.canvas.find_closest(x, y)
    logging.debug('NEAREST %s', nearest)
    for n in nearest:
        tags = global_dependencies.canvas.gettags(n)
        if tags and isinstance(
            global_dependencies.repo.get(tags[0]),
            internal.objects.interfaces.IBoardObjectPen
        ):
            state_ctx[_OBJ_ID] = global_dependencies.repo.get(tags[0]).id
            state_ctx[_PEN_LINE_ID] = PEN_LINE_PREFIX + state_ctx[_OBJ_ID]
            return


def _handle_event(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    # Mouse motion
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return
    if _OBJ_ID not in state_ctx:
        return
    actual_x = int(global_dependencies.canvas.canvasx(event.x))
    actual_y = int(global_dependencies.canvas.canvasy(event.y))
    coord = global_dependencies.canvas.coords(state_ctx[_PEN_LINE_ID])
    coord.append(actual_x)
    coord.append(actual_y)
    global_dependencies.canvas.coords(state_ctx[_PEN_LINE_ID], coord)


def _on_leave(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    obj: internal.objects.interfaces.IBoardObjectPen = global_dependencies.repo.get(
        state_ctx[_OBJ_ID]
    )
    position, points = get_object_points(global_dependencies, obj)
    global_dependencies.controller.edit_points(obj.id, points)


def _predicate_from_root_to_pen(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event
) -> bool:
    # Press left mouse button
    if event.type != tkinter.EventType.ButtonPress or event.num != 1:
        return False
    return global_dependencies.menu.current_state == PEN_MENU_ENTRY_NAME


def _predicate_from_pen_to_root(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event  # noqa
) -> bool:
    # Menu item clicked
    if event.type != tkinter.EventType.VirtualEvent:
        return False
    # Menu select handle before the commands changed
    return global_dependencies.menu.current_state == PEN_MENU_ENTRY_NAME


def _predicate_from_pen_to_pen(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event  # noqa
) -> bool:
    # Release left mouse button
    return event.type == tkinter.EventType.ButtonPress and event.num == 1


def create_state(
    state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
    state = State(_PEN_CREATE_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _PEN_CREATE_STATE_NAME,
        _predicate_from_root_to_pen
    )

    state_machine.add_transition(
        _PEN_CREATE_STATE_NAME,
        _PEN_CREATE_STATE_NAME,
        _predicate_from_pen_to_pen
    )
    state_machine.add_transition(
        _PEN_CREATE_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_pen_to_root
    )
    return state
