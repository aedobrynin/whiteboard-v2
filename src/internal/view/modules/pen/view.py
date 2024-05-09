# import tkinter
#
# import internal.models
# import internal.objects.interfaces
# import internal.view.dependencies
#
# PEN_LINE_PREFIX = 'line'
#
# _WIDTH = 100
#
#
# def create_pen_object(
#     dependencies: internal.view.dependencies.Dependencies,
#     obj: internal.objects.interfaces.IBoardObjectPen
# ) -> int:
#     pen_tag = f'{PEN_LINE_PREFIX}{obj.id}'
#     dependencies.canvas.create_line(
#         get_canvas_points(obj),
#         width=obj.width,
#         fill=obj.color,
#         capstyle=tkinter.ROUND,
#         smooth=True,
#         tags=[obj.id, pen_tag]
#     )
#
#
# def get_canvas_points(
#     obj: internal.objects.interfaces.IBoardObjectPen
# ):
#     points = [obj.position + point for point in obj.points]
#     canvas_points = []
#     for point in points:
#         canvas_points.append(point.x)
#         canvas_points.append(point.y)
#     if len(canvas_points) == 2:
#         canvas_points.extend(canvas_points)
#     return canvas_points
#
#
# def get_object_points(
#     dependencies: internal.view.dependencies.Dependencies,
#     obj: internal.objects.interfaces.IBoardObjectPen
# ):
#     obj: internal.objects.interfaces.IBoardObjectPen
#     coord = dependencies.canvas.coords(obj.id)
#     position = internal.models.Position(coord[0], coord[1], obj.position.z)
#     points = [internal.models.Position(0, 0, obj.position.z)]
#     for i in range(2, len(coord), 2):
#         points.append(internal.models.Position(coord[i], coord[i + 1], obj.position.z) - position)
#     return position, points
