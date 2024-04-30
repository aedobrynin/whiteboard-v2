from __future__ import annotations
from typing import Dict, Optional
import tkinter

from internal.models import Position
from internal.objects.interfaces import IBoardObjectWithPosition
from internal.view.state_machine.impl import State
from internal.view.utils.canvas_repo_obj import get_current_opt
import internal.view.state_machine.interfaces
import internal.view.dependencies

_MOVE_OBJECT_STATE_NAME = 'MOVE_OBJECT'
_LAST_DRAG_EVENT_X = 'last_drag_event_x'
_LAST_DRAG_EVENT_Y = 'last_drag_event_y'
_OBJECT = 'object'


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    global_dependencies.canvas.scan_mark(event.x, event.y)

    x = int(global_dependencies.canvas.canvasx(event.x))
    y = int(global_dependencies.canvas.canvasy(event.y))

    obj: Optional[IBoardObjectWithPosition] = get_current_opt(global_dependencies)
    if not obj:
        return

    state_ctx[_LAST_DRAG_EVENT_X] = x
    state_ctx[_LAST_DRAG_EVENT_Y] = y
    state_ctx[_OBJECT] = obj


def _on_leave(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    _: tkinter.Event
):
    # TODO: Z-Coordinate

    obj: IBoardObjectWithPosition = state_ctx[_OBJECT]
    position: Position = Position(
        state_ctx[_LAST_DRAG_EVENT_X],
        state_ctx[_LAST_DRAG_EVENT_Y],
        1
    )
    # TODO: correct the coord
    global_dependencies.controller.move_object(obj.id, position)
    global_dependencies.canvas.configure(background='white')


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
    obj: IBoardObjectWithPosition = state_ctx[_OBJECT]
    global_dependencies.canvas.move(
        obj.id,
        x - state_ctx[_LAST_DRAG_EVENT_X],
        y - state_ctx[_LAST_DRAG_EVENT_Y]
    )
    state_ctx[_LAST_DRAG_EVENT_X] = x
    state_ctx[_LAST_DRAG_EVENT_Y] = y


def _predicate_from_root_to_move_object(
    global_dependencies: internal.view.dependencies.Dependencies,
    event: tkinter.Event
) -> bool:
    # Motion with Left mouse button pressed
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return False
    cur_obj = get_current_opt(global_dependencies)
    return cur_obj is not None


def _predicate_from_move_object_to_root(
    global_dependencies: internal.view.dependencies.Dependencies,  # noqa
    event: tkinter.Event
) -> bool:
    # Release Left mouse button
    return event.type == tkinter.EventType.ButtonRelease and event.num == 1


def create_state(state_machine: internal.view.state_machine.interfaces.IStateMachine) -> State:
    state = State(_MOVE_OBJECT_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _MOVE_OBJECT_STATE_NAME,
        _predicate_from_root_to_move_object
    )
    state_machine.add_transition(
        _MOVE_OBJECT_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_move_object_to_root
    )
    return state