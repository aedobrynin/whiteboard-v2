# from __future__ import annotations
#
# from dataclasses import dataclass
# from typing import Dict, List
# import tkinter
#
# import internal.objects
# import internal.objects.interfaces
# import internal.models.position
# import internal.view.state_machine.interfaces
# import internal.view.dependencies
# import internal.view.utils
# from internal.view.state_machine.impl import State
# from ..consts.py import GROUP_MENU_ENTRY_NAME
#
# CREATE_GROUP_STATE_NAME = 'CREATE_GROUP'
# FRAME_TKINTER_OBJECT_TAG = 'group_module_frame_object_tag'
# STATE_CONTEXT_OBJ_DICT_KEY = 'group_module_state_context'
#
#
# @dataclass
# class CreateGroupStateContext:
#     drag_start_pos: internal.view.utils.geometry.ScreenPosition
#     frame_was_drawn_before: bool = False
#
#
# def _get_cur_pos(
#     global_dependencies: internal.view.dependencies.Dependencies,
#     event: tkinter.Event
# ) -> internal.view.utils.geometry.ScreenPosition:
#     cur_pos_x = int(global_dependencies.canvas.canvasx(event.x))
#     cur_pos_y = int(global_dependencies.canvas.canvasy(event.y))
#     return internal.view.utils.geometry.ScreenPosition(cur_pos_x, cur_pos_y)
#
#
# def _get_intersected_by_rect_object_ids(
#     global_dependencies: internal.view.dependencies.Dependencies,
#     covering_rect: internal.view.utils.geometry.Rectangle
# ) -> List[str]:
#     ids = []
#     for obj in global_dependencies.repo.get_all():
#         if internal.view.utils.geometry.are_rects_intersecting(
#             internal.view.utils.get_frame_border(global_dependencies, obj.id),
#             covering_rect
#         ):
#             ids.append(obj.id)
#     return ids
#
#
# # does nothing with regular objects
# # for groups: copies group children_ids and destroys the group
# def _get_children_ids(
#     global_dependencies: internal.view.dependencies.Dependencies,
#     object_ids: List[str]
# ) -> List[str]:
#     result_ids = set()
#     for obj_id in object_ids:
#         obj = global_dependencies.repo.get(obj_id)
#         if isinstance(obj, internal.objects.interfaces.IBoardObjectGroup):
#             result_ids.update(obj.children_ids)
#             global_dependencies.repo.delete(obj_id)
#         else:
#             result_ids.add(obj_id)
#     return list(result_ids)
#
#
# def _create_group(
#     global_dependencies: internal.view.dependencies.Dependencies,
#     state_ctx: Dict,
#     event: tkinter.Event
# ):
#     state_ctx_obj: CreateGroupStateContext = state_ctx[STATE_CONTEXT_OBJ_DICT_KEY]
#
#     group_covering_rect = internal.view.utils.geometry.Rectangle(
#         state_ctx_obj.drag_start_pos, _get_cur_pos(global_dependencies, event)
#     )
#     intersected_object_ids = _get_intersected_by_rect_object_ids(
#         global_dependencies,
#         group_covering_rect
#     )
#     if len(intersected_object_ids) < 2:
#         return
#     children_ids = _get_children_ids(global_dependencies, intersected_object_ids)
#     assert len(children_ids) >= 2
#
#     # There we create a new group all the time even if there is only one group intersected
#     # It can be optimized later: issue #32
#
#     global_dependencies.controller.create_object(
#         internal.objects.BoardObjectType.GROUP,
#         children_ids=children_ids
#     )
#
#
# def _predicate_from_root_to_create_group(
#     global_dependencies: internal.view.dependencies.Dependencies,
#     event: tkinter.Event
# ):
#     # Press Left mouse button with sticker menu state
#     return (
#         event.type == tkinter.EventType.ButtonPress
#         and event.num == 1
#         and global_dependencies.menu.current_state == GROUP_MENU_ENTRY_NAME
#     )
#
#
# def _handle_event(
#     global_dependencies: internal.view.dependencies.Dependencies,
#     state_ctx: Dict,
#     event: tkinter.Event
# ):
#     # Motion with Left mouse button pressed
#     if event.type != tkinter.EventType.Motion or event.state & (1 << 8) == 0:
#         return
#
#     cur_pos = _get_cur_pos(global_dependencies, event)
#
#     if STATE_CONTEXT_OBJ_DICT_KEY not in state_ctx:
#         # We are first time here
#         state_ctx[STATE_CONTEXT_OBJ_DICT_KEY] = CreateGroupStateContext(
#             drag_start_pos=cur_pos, frame_was_drawn_before=False
#         )
#         return
#
#     state_ctx_obj: CreateGroupStateContext = state_ctx[STATE_CONTEXT_OBJ_DICT_KEY]
#     rect = internal.view.utils.geometry.Rectangle(
#         state_ctx_obj.drag_start_pos,
#         cur_pos
#     ).as_tkinter_rect()
#     if state_ctx_obj.frame_was_drawn_before:
#         global_dependencies.canvas.coords(FRAME_TKINTER_OBJECT_TAG, *rect)
#     else:
#         FRAME_COLOR = 'black'
#         FRAME_WIDTH = 2
#         global_dependencies.canvas.create_rectangle(
#             *rect, outline=FRAME_COLOR, width=FRAME_WIDTH, tags=FRAME_TKINTER_OBJECT_TAG
#         )
#         state_ctx_obj.frame_was_drawn_before = True
#
#
# def _on_leave(
#     global_dependencies: internal.view.dependencies.Dependencies,
#     state_ctx: Dict,
#     event: tkinter.Event
# ):
#     if STATE_CONTEXT_OBJ_DICT_KEY in state_ctx:
#         _create_group(global_dependencies, state_ctx, event)
#     global_dependencies.canvas.delete(FRAME_TKINTER_OBJECT_TAG)
#     global_dependencies.menu.set_selected_state()
#
#
# def _predicate_from_create_group_to_root(
#     global_dependencies: internal.view.dependencies.Dependencies,
#     event: tkinter.Event
# ) -> bool:
#     # Release left mouse button
#     return event.type == tkinter.EventType.ButtonRelease and event.num == 1
#
#
# def create_state(state_machine):
#     state = State(CREATE_GROUP_STATE_NAME)
#     state.set_event_handler(_handle_event)
#     state.set_on_leave(_on_leave)
#     state_machine.add_transition(
#         internal.view.state_machine.interfaces.ROOT_STATE_NAME,
#         CREATE_GROUP_STATE_NAME,
#         _predicate_from_root_to_create_group,
#     )
#     state_machine.add_transition(
#         CREATE_GROUP_STATE_NAME,
#         internal.view.state_machine.interfaces.ROOT_STATE_NAME,
#         _predicate_from_create_group_to_root,
#     )
#     return state
