# from typing import Optional
#
# import internal.objects.interfaces
# import internal.objects.events
# import internal.view.dependencies
# import internal.view.utils
# from .consts.py import GROUP_PREFIX
#
#
# def create_group_object(
#     dependencies: internal.view.dependencies.Dependencies,
#     obj: internal.objects.interfaces.IBoardObjectGroup
# ) -> None:
#     invisible_rect = _get_invisible_rect(dependencies, obj.children_ids)
#     dependencies.canvas.create_rectangle(
#         *invisible_rect.as_tkinter_rect(),
#         outline='green',  # TODO: remove after tests
#         fill='gray',  # do not remove
#         stipple='@internal/view/modules/group/xbms/transparent.xbm',
#         width=2,
#         tags=[
#             obj.id,
#             GROUP_PREFIX + obj.id
#         ],
#     )
#     dependencies.canvas.tag_raise(obj.id)
#     for child_id in obj.children_ids:
#         dependencies.canvas.addtag_withtag(obj.id, child_id)
#
#
# def _subscribe(
#     dependencies: internal.view.dependencies.Dependencies,
#     obj: internal.objects.interfaces.IBoardObjectGroup
# ):
#     for child_id in obj.children_ids:
#         dependencies.pub_sub_broker.subscribe(
#             obj.id,
#             child_id,
#             internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_SIZE,
#             lambda *_: _child_move(dependencies, child_id)
#         )
#
#
# def _child_move(
#     dependencies: internal.view.dependencies.Dependencies,
#     obj_id: internal.objects.interfaces.ObjectId
# ):
#     obj: Optional[
#         internal.objects.interfaces.IBoardObjectWithPosition
#     ] = dependencies.repo.get(obj_id)
#     if obj:
#         dependencies.canvas.moveto(
#             obj_id,
#             obj.position.x,
#             obj.position.y
#         )
#
#
# def _get_invisible_rect(
#     dependencies: internal.view.dependencies.Dependencies,
#     children_ids: tuple[internal.objects.interfaces.ObjectId]
# ) -> internal.view.utils.geometry.Rectangle:
#     invisible_rect = None
#     for child_id in children_ids:
#         child_rect = internal.view.utils.object_border.get_frame_border(
#             dependencies, child_id
#         )
#         invisible_rect = internal.view.utils.geometry.get_min_containing_rect(
#             invisible_rect, child_rect
#         )
#     assert invisible_rect is not None
#     return invisible_rect
