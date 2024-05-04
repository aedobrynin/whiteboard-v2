import internal.objects.interfaces
import internal.view.dependencies

CARD_TEXT_PREFIX = 'card_text'
CARD_NOTE_PREFIX = 'card_note'

_WIDTH = 100


def create_card_object(
    dependencies: internal.view.dependencies.Dependencies,
    obj: internal.objects.interfaces.IBoardObjectCard
) -> int:
    text_tag = f'{CARD_TEXT_PREFIX}{obj.id}'
    note_tag = f'{CARD_NOTE_PREFIX}{obj.id}'
    dependencies.canvas.create_text(
        obj.position.x,
        obj.position.y,
        text=obj.text,
        fill=obj.font.color,
        tags=[obj.id, text_tag],
        width=_WIDTH,
        font=(obj.font.family, int(obj.font.size), obj.font.weight, obj.font.slant)
    )

    arr = create_note_coord(dependencies, obj.id, _WIDTH)
    dependencies.canvas.create_rectangle(
        arr,
        fill=obj.color,
        tags=[obj.id, note_tag],
    )
    dependencies.canvas.tag_lower(note_tag, text_tag)
    adjust_font(dependencies, obj)


def create_note_coord(
    dependencies: internal.view.dependencies.Dependencies,
    obj_id: internal.objects.interfaces.ObjectId,
    width: int
):
    args = dependencies.canvas.bbox(obj_id)
    arr = [args[i] for i in range(len(args))]
    arr[0] = (arr[2] + arr[0] - width) / 2
    arr[1] = (arr[1] + arr[3] - width) / 2
    arr[2] = arr[0] + width
    arr[3] = arr[1] + width
    return arr


def _get_font(
    obj: internal.objects.interfaces.IBoardObjectCard,
) -> tuple:
    return obj.font.family, obj.font.size, obj.font.weight, obj.font.slant


def adjust_font(
    dependencies: internal.view.dependencies.Dependencies,
    obj: internal.objects.interfaces.IBoardObjectCard,
    larger=True
):
    text_tag = f'{CARD_TEXT_PREFIX}{obj.id}'
    width = int(dependencies.canvas.itemcget(text_tag, 'width'))
    _, y1, _, y2 = dependencies.canvas.bbox(text_tag)
    floated_size = float(obj.font.size)
    if larger:
        while abs(y1 - y2) > width:
            floated_size /= 1.05
            dependencies.controller.edit_font(
                obj_id=obj.id, size=int(floated_size)
            )
            dependencies.canvas.itemconfig(text_tag, font=_get_font(obj))
            _, y1, _, y2 = dependencies.canvas.bbox(text_tag)
    else:
        while abs(y1 - y2) < width * 0.7:
            floated_size *= 1.05
            dependencies.controller.edit_font(
                obj_id=obj.id, size=int(floated_size)
            )
            dependencies.canvas.itemconfig(text_tag, font=_get_font(obj))
            _, y1, _, y2 = dependencies.canvas.bbox(text_tag)
            y1 = dependencies.canvas.canvasx(y1)
            y2 = dependencies.canvas.canvasy(y2)
