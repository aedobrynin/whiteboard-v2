import internal.objects.interfaces
import internal.view.dependencies
from .geometry import Rectangle

_OFFSET = 3
_PADDING = 50


# def _get_frame_border(
#     dependencies: internal.view.dependencies.Dependencies,
#     obj_id: internal.objects.interfaces.ObjectId
# ) -> Rectangle:
#     obj_frame = list(dependencies.canvas.bbox(obj_id))
#     obj_frame[0] -= _OFFSET
#     obj_frame[1] -= _OFFSET
#     obj_frame[2] += _OFFSET
#     obj_frame[3] += _OFFSET
#     return internal.view.utils.geometry.Rectangle.from_tkinter_rect(tuple(obj_frame))
#
#
# def _aligned(
#     dependencies: internal.view.dependencies.Dependencies,
#     obj_id: internal.objects.interfaces.ObjectId
# ):
#     return bool(dependencies.canvas.gettags(obj_id))


def aligning(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId
):
    remove_aligning(dependencies, obj_id)
    obj_frame = list(dependencies.canvas.bbox(obj_id))

    top = dependencies.canvas.find_overlapping(obj_frame[0] - _PADDING,
                                               obj_frame[1] - _PADDING,
                                               obj_frame[2] + _PADDING,
                                               obj_frame[1])
    # key=lambda x: dependencies.canvas.coords(x)[3])

    COLOR = 'blue'
    ID = f'line{obj_id}'
    for item in top:
        tags = dependencies.canvas.gettags(item)
        if tags[0] == obj_id:
            continue

        obj_x1, obj_y1, obj_x2, obj_y2 = dependencies.canvas.bbox(tags[0])
        if not (obj_x1 in [obj_frame[0], obj_frame[2]] or obj_x2 in [obj_frame[0], obj_frame[2]]):
            continue

        if obj_frame[0] == obj_x1:
            dependencies.canvas.create_line(obj_x1, obj_y1, obj_frame[0], obj_frame[3], tags=[ID],
                                            fill=COLOR)
            break
        if obj_frame[0] == obj_x2:
            dependencies.canvas.create_line(obj_x2, obj_y1, obj_frame[0], obj_frame[3], tags=[ID],
                                            fill=COLOR)
            break
        if obj_frame[1] == obj_x1:
            dependencies.canvas.create_line(obj_x1, obj_y1, obj_frame[1], obj_frame[3], tags=[ID],
                                            fill=COLOR)
            break
        if obj_frame[1] == obj_x2:
            dependencies.canvas.create_line(obj_x2, obj_y1, obj_frame[1], obj_frame[3], tags=[ID],
                                            fill=COLOR)
            break
    else:

        bottom = dependencies.canvas.find_overlapping(obj_frame[0] - _PADDING,
                                                      obj_frame[3],
                                                      obj_frame[2] + _PADDING,
                                                      obj_frame[3] + _PADDING)
        # key=lambda x: dependencies.canvas.coords(x)[1])
        for item in bottom:
            tags = dependencies.canvas.gettags(item)
            if tags[0] == obj_id:
                continue
            obj_x1, obj_y1, obj_x2, obj_y2 = dependencies.canvas.bbox(tags[0])
            if not (obj_x1 in [obj_frame[0], obj_frame[2]] or obj_x2 in [obj_frame[0], obj_frame[2]]):
                continue

            if obj_frame[0] == obj_x1:
                dependencies.canvas.create_line(obj_frame[0], obj_frame[3], obj_x1, obj_y1, tags=[ID],
                                                fill=COLOR)
                break
            if obj_frame[0] == obj_x2:
                dependencies.canvas.create_line(obj_frame[0], obj_frame[3], obj_x2, obj_y1, tags=[ID],
                                                fill=COLOR)
                break
            if obj_frame[2] == obj_x1:
                dependencies.canvas.create_line(obj_frame[2], obj_frame[3], obj_x1, obj_y1, tags=[ID],
                                                fill=COLOR)
                break
            if obj_frame[2] == obj_x2:
                dependencies.canvas.create_line(obj_frame[2], obj_frame[3], obj_x2, obj_y1, tags=[ID],
                                                fill=COLOR)
                break

        left = dependencies.canvas.find_overlapping(obj_frame[0] - _PADDING,
                                                    obj_frame[1] - _PADDING,
                                                    obj_frame[0],
                                                    obj_frame[3] + _PADDING)
        # key=lambda x: dependencies.canvas.coords(x)[2])
        for item in left:
            tags = dependencies.canvas.gettags(item)
            if tags[0] == obj_id:
                continue
            obj_x1, obj_y1, obj_x2, obj_y2 = dependencies.canvas.bbox(tags[0])
            if not (obj_y1 in [obj_frame[1], obj_frame[3]] or obj_y2 in [obj_frame[1], obj_frame[3]]):
                continue

            if obj_frame[1] == obj_y1:
                dependencies.canvas.create_line(obj_x1, obj_y1, obj_frame[2], obj_frame[1], tags=[ID],
                                                fill=COLOR)
                break
            if obj_frame[1] == obj_y2:
                dependencies.canvas.create_line(obj_x1, obj_y2, obj_frame[2], obj_frame[1], tags=[ID],
                                                fill=COLOR)
                break
            if obj_frame[3] == obj_y1:
                dependencies.canvas.create_line(obj_x1, obj_y1, obj_frame[2], obj_frame[3], tags=[ID],
                                                fill=COLOR)
                break
            if obj_frame[3] == obj_y2:
                dependencies.canvas.create_line(obj_x1, obj_y2, obj_frame[2], obj_frame[3], tags=[ID],
                                                fill=COLOR)
                break
        else:

            right = dependencies.canvas.find_overlapping(obj_frame[2],
                                                         obj_frame[1] - _PADDING,
                                                         obj_frame[2] + _PADDING,
                                                         obj_frame[3] + _PADDING)
            # key=lambda x: dependencies.canvas.coords(x)[0])
            for item in right:
                tags = dependencies.canvas.gettags(item)
                if tags[0] == obj_id:
                    continue
                obj_x1, obj_y1, obj_x2, obj_y2 = dependencies.canvas.bbox(tags[0])
                if not (obj_y1 in [obj_frame[1], obj_frame[3]] or obj_y2 in [obj_frame[1], obj_frame[3]]):
                    continue

                if obj_frame[1] == obj_y1:
                    dependencies.canvas.create_line(obj_frame[2], obj_frame[1], obj_x1, obj_y1, tags=[ID],
                                                    fill=COLOR)
                    break
                if obj_frame[1] == obj_y2:
                    dependencies.canvas.create_line(obj_frame[2], obj_frame[1], obj_x1, obj_y2, tags=[ID],
                                                    fill=COLOR)
                    break
                if obj_frame[3] == obj_y1:
                    dependencies.canvas.create_line(obj_frame[2], obj_frame[3], obj_x1, obj_y1, tags=[ID],
                                                    fill=COLOR)
                    break
                if obj_frame[3] == obj_y2:
                    dependencies.canvas.create_line(obj_frame[2], obj_frame[3], obj_x1, obj_y2, tags=[ID],
                                                    fill=COLOR)
                    break


def remove_aligning(
        dependencies: internal.view.dependencies.Dependencies,
        obj_id: internal.objects.interfaces.ObjectId
):
    obj_id = f'line{obj_id}'
    dependencies.canvas.delete(obj_id)
