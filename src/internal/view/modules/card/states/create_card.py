# from __future__ import annotations
# from typing import Dict
# import tkinter
#
# import internal.objects
# import internal.models.position
# from internal.view.state_machine.impl import State
# import internal.view.state_machine.interfaces
# import internal.view.dependencies
#
# CARD_MENU_ENTRY_NAME = 'card'
# CREATE_CARD_STATE_NAME = 'CREATE_CARD'
#
#
# def _predicate_from_root_to_create_card(
#     global_dependencies: internal.view.dependencies.Dependencies,
#     event: tkinter.Event
# ) -> bool:
#     # Press Left mouse button with text menu state
#     if event.type != tkinter.EventType.ButtonPress:
#         return False
#     if event.num != 1:
#         return False
#     if global_dependencies.menu.current_state != CARD_MENU_ENTRY_NAME:
#         return False
#
#     actual_x = int(global_dependencies.canvas.canvasx(event.x))
#     actual_y = int(global_dependencies.canvas.canvasy(event.y))
#
#     global_dependencies.controller.create_object(
#         internal.objects.BoardObjectType.CARD,
#         position=internal.models.position.Position(actual_x, actual_y, z=1)
#     )
#     return True
#
#
# def _on_leave(
#     global_dependencies: internal.view.dependencies.Dependencies,
#     state_ctx: Dict,
#     event: tkinter.Event
# ):
#     global_dependencies.menu.set_selected_state()
#
#
# def _predicate_from_create_card_to_root(
#     global_dependencies: internal.view.dependencies.Dependencies,
#     event: tkinter.Event
# ) -> bool:
#     # Release left mouse button
#     return event.type == tkinter.EventType.ButtonRelease and event.num == 1
#
#
# def create_state(
#     state_machine: internal.view.state_machine.interfaces.IStateMachine
# ) -> State:
#     state = State(CARD_MENU_ENTRY_NAME)
#     state.set_on_leave(_on_leave)
#     state_machine.add_transition(
#         internal.view.state_machine.interfaces.ROOT_STATE_NAME,
#         CARD_MENU_ENTRY_NAME,
#         _predicate_from_root_to_create_card
#     )
#     state_machine.add_transition(
#         CARD_MENU_ENTRY_NAME,
#         internal.view.state_machine.interfaces.ROOT_STATE_NAME,
#         _predicate_from_create_card_to_root
#     )
#     return state
