from __future__ import annotations

import tkinter
from typing import Dict, Optional

import internal.view.dependencies
import internal.view.state_machine.interfaces
from internal.models import Position
from internal.view.modules.connector import ConnectorObject
from internal.view.objects.interfaces import IViewObject
from internal.view.state_machine.impl import State

_MOVE_OBJECT_STATE_NAME = 'MOVE_OBJECT'
_LAST_DRAG_EVENT_X = 'last_drag_event_x'
_LAST_DRAG_EVENT_Y = 'last_drag_event_y'
_FIRST_DRAG_EVENT_X = 'first_drag_event_x'
_FIRST_DRAG_EVENT_Y = 'first_drag_event_y'
_OBJ_ID = 'obj_id'


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    x = int(global_dependencies.canvas.canvasx(event.x))
    y = int(global_dependencies.canvas.canvasy(event.y))

    obj: Optional[IViewObject] = global_dependencies.objects_storage.get_current_opt(
        global_dependencies
    )
    if not obj:
        return

    state_ctx[_LAST_DRAG_EVENT_X] = x
    state_ctx[_LAST_DRAG_EVENT_Y] = y
    state_ctx[_FIRST_DRAG_EVENT_X] = x
    state_ctx[_FIRST_DRAG_EVENT_Y] = y
    state_ctx[_OBJ_ID] = obj.id


def _on_leave(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    # TODO: Z-Coordinate
    diff: Position = Position(
        state_ctx[_LAST_DRAG_EVENT_X] - state_ctx[_FIRST_DRAG_EVENT_X],
        state_ctx[_LAST_DRAG_EVENT_Y] - state_ctx[_FIRST_DRAG_EVENT_Y],
        0
    )
    # TODO: we send difference, if 2 people uses it collapse
    global_dependencies.controller.move_object(
        state_ctx[_OBJ_ID], diff
    )
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
    global_dependencies.canvas.move(
        state_ctx[_OBJ_ID],
        x - state_ctx[_LAST_DRAG_EVENT_X],
        y - state_ctx[_LAST_DRAG_EVENT_Y]
    )
    state_ctx[_LAST_DRAG_EVENT_X] = x
    state_ctx[_LAST_DRAG_EVENT_Y] = y
    # TODO: because we notify only when view-move done, connector doesnt update correctly curve
    other_tags = global_dependencies.canvas.gettags(state_ctx[_OBJ_ID])
    for tag in other_tags:
        obj = global_dependencies.objects_storage.get_opt_by_id(tag)
        if obj and isinstance(obj, ConnectorObject):
            obj.curve(global_dependencies)


def _predicate_from_root_to_move_object(
    global_dependencies: internal.view.dependencies.Dependencies,
    event: tkinter.Event
) -> bool:
    # Motion with Left mouse button pressed
    if global_dependencies.menu.current_state != global_dependencies.menu.MENU_ROOT_STATE:
        return False
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return False
    cur_obj = global_dependencies.objects_storage.get_current_opt(
        global_dependencies
    )
    if cur_obj is None:
        return False
    return not isinstance(cur_obj, ConnectorObject)


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
