from __future__ import annotations
from typing import Dict, Optional
import tkinter

from internal.models import Position
from internal.objects.interfaces import IBoardObjectWithPosition, IBoardObjectTable
from internal.objects.events import EVENT_TYPE_OBJECT_MOVED
from internal.view.modules.table.table_view import add_object
from internal.view.state_machine.impl import State
from internal.view.utils.canvas_repo_obj import get_current_opt
import internal.view.state_machine.interfaces
import internal.view.dependencies
import internal.view.modules.table.table_view

_MOVE_OBJECT_STATE_NAME = 'MOVE_OBJECT'
_INITIAL_POSITION = 'obj_position'
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
    global_dependencies.canvas.scan_mark(event.x, event.y)

    x = int(global_dependencies.canvas.canvasx(event.x))
    y = int(global_dependencies.canvas.canvasy(event.y))

    obj: Optional[IBoardObjectWithPosition] = get_current_opt(global_dependencies)
    if not obj:
        return

    state_ctx[_LAST_DRAG_EVENT_X] = x
    state_ctx[_LAST_DRAG_EVENT_Y] = y

    state_ctx[_FIRST_DRAG_EVENT_X] = x
    state_ctx[_FIRST_DRAG_EVENT_Y] = y
    state_ctx[_INITIAL_POSITION] = obj.position
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
    position = state_ctx[_INITIAL_POSITION] + diff
    # TODO: correct the coord
    global_dependencies.controller.move_object(state_ctx[_OBJ_ID], position)
    global_dependencies.canvas.configure(background='white')

    obj = global_dependencies.repo.get(state_ctx[_OBJ_ID])
    if not obj:
        return
    # for table
    if isinstance(obj, internal.objects.interfaces.IBoardObjectTable):
        obj: IBoardObjectTable = obj
        if not obj:
            return
        for (id, _) in obj.linked_objects.items():
            child: Optional[IBoardObjectWithPosition] = global_dependencies.repo.get(id)
            global_dependencies.controller.move_object(id, child.position + diff)

        return

    parent_obj_id, coords = add_object(global_dependencies, obj, position)
    if parent_obj_id:
        global_dependencies.controller.add_object_to(state_ctx[_OBJ_ID], parent_obj_id, coords)

        global_dependencies.pub_sub_broker.subscribe(
                parent_obj_id,
                obj.id,
                EVENT_TYPE_OBJECT_MOVED,
                lambda *_: internal.view.modules.table.view.unsub(global_dependencies, obj, parent_obj_id)
            )





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

    obj = global_dependencies.repo.get(state_ctx[_OBJ_ID])
    # for table
    if isinstance(obj, internal.objects.interfaces.IBoardObjectTable):
        obj: IBoardObjectTable = obj
        if not obj:
            return
        for (key, _) in obj.linked_objects.items():
            global_dependencies.canvas.move(
                key,
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
