from __future__ import annotations

from typing import Dict
import tkinter

import internal.models
import internal.objects.interfaces
import internal.view.dependencies
import internal.view.state_machine.interfaces
from internal.view.state_machine.impl import State
from ..consts import PEN_MENU_ENTRY_NAME, PEN_CREATE_STATE_NAME

_CURRENT_LINE_ID = 'line_id'


def _from_canvas_coord_to_object_points(points: list[int]):
    positions = []
    # TODO: Z-coordinate
    for i in range(1, len(points), 2):
        positions.append(internal.models.Position(points[i - 1], points[i], 1))
    return positions


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event,
):
    x = global_dependencies.canvas.canvasx(event.x)
    y = global_dependencies.canvas.canvasy(event.y)
    # TODO: the project should have default configs like WIDTH of line
    # We create pseudo-line, then on leave we delete this line and create line from repo
    state_ctx[_CURRENT_LINE_ID] = global_dependencies.canvas.create_line(
        [x, y, x, y],
        width=internal.objects.interfaces.IBoardObjectPen.DEFAULT_WIDTH,
        fill=internal.objects.interfaces.IBoardObjectPen.DEFAULT_COLOR,
        capstyle=tkinter.ROUND,
        smooth=True,
    )


def _handle_event(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event,
):
    # Mouse motion
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return
    if _CURRENT_LINE_ID not in state_ctx:
        return
    actual_x = int(global_dependencies.canvas.canvasx(event.x))
    actual_y = int(global_dependencies.canvas.canvasy(event.y))
    coord = global_dependencies.canvas.coords(state_ctx[_CURRENT_LINE_ID])
    coord.append(actual_x)
    coord.append(actual_y)
    global_dependencies.canvas.coords(state_ctx[_CURRENT_LINE_ID], coord)


def _on_leave(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event,
):
    if _CURRENT_LINE_ID not in state_ctx:
        return
    points = global_dependencies.canvas.coords(state_ctx[_CURRENT_LINE_ID])
    positions = _from_canvas_coord_to_object_points(points)
    global_dependencies.controller.create_object(
        internal.objects.BoardObjectType.PEN, points=positions
    )
    global_dependencies.canvas.delete(state_ctx[_CURRENT_LINE_ID])


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
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(state_machine: internal.view.state_machine.interfaces.IStateMachine) -> State:
    state = State(PEN_CREATE_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        PEN_CREATE_STATE_NAME,
        _predicate_from_root_to_pen,
    )
    state_machine.add_transition(
        PEN_CREATE_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_pen_to_root,
    )
    return state