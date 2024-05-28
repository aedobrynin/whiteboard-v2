from __future__ import annotations

import logging
import tkinter
from typing import Dict

import internal.models
import internal.objects.interfaces
import internal.view.dependencies
import internal.view.state_machine.interfaces
from internal.view.objects.interfaces import IViewObject
from internal.view.state_machine.impl import State
from ..connector_view import ConnectorObject
from ..consts import CONNECTOR_CREATE_STATE_NAME, CONNECTOR_MENU_ENTRY_NAME

_CURRENT_CONNECTOR_ID = 'connector_id'
_START_ID = 'start_id'
_END_ID = 'end_id'


def _on_enter(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    cur_obj = global_dependencies.objects_storage.get_current(
        global_dependencies
    )
    state_ctx[_START_ID] = cur_obj.id
    x = global_dependencies.canvas.canvasx(event.x)
    y = global_dependencies.canvas.canvasy(event.y)
    # TODO: the project should have default configs like WIDTH of line
    # We create pseudo-line, then on leave we delete this line and create line from repo
    state_ctx[_CURRENT_CONNECTOR_ID] = global_dependencies.canvas.create_line(
        [x, y, x, y],
        width=internal.objects.interfaces.IBoardObjectConnector.DEFAULT_WIDTH,
        fill=internal.objects.interfaces.IBoardObjectConnector.DEFAULT_COLOR,
        capstyle=tkinter.ROUND,
        smooth=True
    )


def _handle_event(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    # Mouse motion
    if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
        return
    if _CURRENT_CONNECTOR_ID not in state_ctx:
        return
    actual_x = int(global_dependencies.canvas.canvasx(event.x))
    actual_y = int(global_dependencies.canvas.canvasy(event.y))
    coord = global_dependencies.canvas.coords(state_ctx[_CURRENT_CONNECTOR_ID])
    coord = [coord[0], coord[1], actual_x, actual_y]
    global_dependencies.canvas.coords(state_ctx[_CURRENT_CONNECTOR_ID], coord)


def _on_leave(
    global_dependencies: internal.view.dependencies.Dependencies,
    state_ctx: Dict,
    event: tkinter.Event
):
    if _CURRENT_CONNECTOR_ID not in state_ctx:
        return
    actual_x = int(global_dependencies.canvas.canvasx(event.x))
    actual_y = int(global_dependencies.canvas.canvasy(event.y))

    ids = global_dependencies.canvas.find_overlapping(
        actual_x, actual_y, actual_x, actual_y
    )
    cur_obj: IViewObject = None
    for id in ids:  # noqa
        tag = global_dependencies.canvas.gettags(id)
        cur_obj = global_dependencies.objects_storage.get_opt_by_id(tag[0])
        if cur_obj:
            break

    if cur_obj is None:
        global_dependencies.canvas.delete(state_ctx[_CURRENT_CONNECTOR_ID])
        return
    if isinstance(cur_obj, ConnectorObject):
        global_dependencies.canvas.delete(state_ctx[_CURRENT_CONNECTOR_ID])
        return
    if cur_obj.id == state_ctx[_START_ID]:
        global_dependencies.canvas.delete(state_ctx[_CURRENT_CONNECTOR_ID])
        return
    state_ctx[_END_ID] = cur_obj.id
    logging.debug('trying to create connector')
    global_dependencies.controller.create_object(
        internal.objects.BoardObjectType.CONNECTOR,
        start_id=state_ctx[_START_ID],
        end_id=state_ctx[_END_ID]
    )
    logging.debug('trying to create connector')
    global_dependencies.canvas.delete(state_ctx[_CURRENT_CONNECTOR_ID])
    global_dependencies.menu.set_selected_state()


def _predicate_from_root_to_connector(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event
) -> bool:
    # Press left mouse button
    if global_dependencies.menu.current_state != CONNECTOR_MENU_ENTRY_NAME:
        return False
    if event.type != tkinter.EventType.ButtonPress or event.num != 1:
        return False
    cur_obj = global_dependencies.objects_storage.get_current_opt(
        global_dependencies
    )
    if cur_obj is None:
        return False
    return not isinstance(cur_obj, ConnectorObject)


def _predicate_from_connector_to_root(
    global_dependencies: internal.view.dependencies.Dependencies, event: tkinter.Event  # noqa
) -> bool:
    # Menu item clicked
    if event.type != tkinter.EventType.ButtonRelease or event.num != 1:
        return False
    return global_dependencies.menu.current_state == CONNECTOR_MENU_ENTRY_NAME


def create_state(
    state_machine: internal.view.state_machine.interfaces.IStateMachine
) -> State:
    state = State(CONNECTOR_CREATE_STATE_NAME)
    state.set_on_enter(_on_enter)
    state.set_event_handler(_handle_event)
    state.set_on_leave(_on_leave)
    state_machine.add_transition(
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        CONNECTOR_CREATE_STATE_NAME,
        _predicate_from_root_to_connector
    )
    state_machine.add_transition(
        CONNECTOR_CREATE_STATE_NAME,
        internal.view.state_machine.interfaces.ROOT_STATE_NAME,
        _predicate_from_connector_to_root
    )
    return state
