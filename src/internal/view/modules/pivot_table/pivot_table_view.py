import tkinter
from tkinter import ttk

import internal.objects.interfaces
import internal.view.dependencies
from internal.models import Position
from .toplevel import Window

NAME = 'name'


def open_window(
    dependencies: internal.view.dependencies.Dependencies
) -> (tkinter.Toplevel, ttk.Entry):
    window = Window(dependencies)
    window.title('New attribute')

    label = ttk.Label(window, text='Name')
    label.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    entry = window.add_entry(NAME)
    entry.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

    def dummy():
        window.saved = False
        dependencies.canvas.event_generate('<Deactivate>')
        window.destroy()

    window.protocol('WM_DELETE_WINDOW', dummy)

    def after_add():
        window.saved = True
        dependencies.canvas.event_generate('<Deactivate>')
        window.destroy()

    bt = ttk.Button(window, text='Save', command=after_add)
    bt.grid(row=4, column=1, padx=5, pady=5, sticky='nsew')
    return window


def show_axis(
    dependencies: internal.view.dependencies.Dependencies
):
    # create new window for table view
    # window = tkinter.Toplevel(dependencies.canvas, width=1000, height=500)
    window = Window(dependencies)
    window.title('Chose axis')

    columns = all_attrs(dependencies)

    for i, col in enumerate(columns):
        label = ttk.Label(window, text=col)
        label.grid(row=i, column=0, padx=5, pady=5, sticky='nsew')

        vals = ['None', 'X', 'Y']
        entry = window.add_combobox(col, vals)
        entry.grid(row=i, column=1, padx=5, pady=5, sticky='nsew')

    def dummy():
        window.saved = False
        dependencies.canvas.event_generate('<Property>')
        window.destroy()

    window.protocol('WM_DELETE_WINDOW', dummy)

    def show_table():
        window.saved = True
        dependencies.canvas.event_generate('<Deactivate>')
        window.destroy()

    button = ttk.Button(window, text='Show Table view', command=show_table)
    button.grid(row=len(columns), column=1, padx=5, pady=5, sticky='nsew')
    return window


def all_attrs(
    dependencies: internal.view.dependencies.Dependencies
):
    attributes = set()
    for obj in dependencies.repo.get_all():
        if not isinstance(obj, internal.objects.interfaces.IBoardObjectCard):
            continue
        card: internal.objects.interfaces.IBoardObjectCard = obj
        attributes = attributes.union(set(list(card.attribute.keys())))
    return list(attributes)


def get_options(
    dependencies: internal.view.dependencies.Dependencies,
    name: str

):
    options = {''}
    for obj in dependencies.repo.get_all():
        if not isinstance(obj, internal.objects.interfaces.IBoardObjectCard):
            continue
        card: internal.objects.interfaces.IBoardObjectCard = obj
        options.add(card.attribute.get(name, ''))
    return list(options)


def draw_table(
    dependencies: internal.view.dependencies.Dependencies,
    val_dic: dict
):
    w = Window(dependencies, canvas=True)
    w.title('Pivot table')

    def dummy():
        w.saved = False
        dependencies.canvas.event_generate('<Property>')
        w.destroy()

    w.protocol('WM_DELETE_WINDOW', dummy)

    x_list = []
    y_list = []
    for name, axis in val_dic.items():
        if axis == 'X':
            x_list.append(name)
        elif axis == 'Y':
            y_list.append(name)

    x_options = dict()
    col_num = 1
    y_options = dict()
    row_num = 1
    for attr in x_list:
        x_options[attr] = get_options(dependencies, attr)
        col_num *= len(x_options[attr])
    pure_col_n = col_num

    for attr in y_list:
        y_options[attr] = get_options(dependencies, attr)
        row_num *= len(y_options[attr])
    pure_row_n = row_num

    col_num += len(y_list)
    row_num += len(x_list)
    height = (500 + 50) / row_num
    width = (1000 + 50) / col_num

    start_x = 25
    start_y = 25

    [
        w.canvas.create_line(
            start_x + i * width, start_y,
            start_x + i * width,
            start_y + height * row_num
        ) for i in range(0, col_num + 1)
    ]
    [
        w.canvas.create_line(
            start_x,
            start_y + i * height,
            start_x + width * col_num,
            start_y + i * height
        ) for i in range(0, row_num + 1)
    ]
    reps_x = 1
    for i, atr in enumerate(x_list):
        opt_n = len(x_options[atr])
        interval = pure_col_n / (opt_n * reps_x)
        for j, opt in enumerate(x_options[atr]):
            [w.canvas.create_text(
                start_x + (interval * (opt_n * m + j) + len(y_list) + 1 / 2) * width,
                start_y + (i + 1 / 2) * height,
                text=atr + '.' + opt) for m in range(reps_x)]
        reps_x *= opt_n

    reps_y = 1

    for i, atr in enumerate(y_list):
        opt_n = len(y_options[atr])
        interval = pure_row_n / (opt_n * reps_y)
        for j, opt in enumerate(y_options[atr]):
            [w.canvas.create_text(start_x + (i + 1 / 2) * width,
                                  start_y + (interval * (opt_n * m + j) + len(
                                      x_list) + 1 / 2) * height,
                                  text=atr + '.' + opt) for m in range(reps_y)]
        reps_y *= opt_n

    obj_coords_x = dict()
    obj_coords_y = dict()
    for obj in dependencies.repo.get_all():
        if not isinstance(obj, internal.objects.interfaces.IBoardObjectCard):
            continue
        card: internal.objects.interfaces.IBoardObjectCard = obj
        obj_coords_x[card.id] = 0
        reps_x = 1
        for x in x_list:
            val = obj.attribute.get(x, '')
            obj_coords_x[card.id] += x_options[x].index(val) * reps_x
            reps_x *= len(x_options[x]) + 1

        obj_coords_y[card.id] = 0
        reps_y = 1
        for y in y_list:
            val = obj.attribute.get(y, '')
            obj_coords_y[card.id] += y_options[y].index(val) * reps_y
            reps_y *= len(y_options[y]) + 1

        create_card_object(
            w.canvas, card,
            ((obj_coords_x[card.id] + len(y_list) + .5) * width + start_x,
             (obj_coords_y[card.id] + len(x_list) + 0.5) * height + start_y)
        )

    return w, x_list, x_options, y_list, y_options, width, height


def get_attr_from_position(
    position: Position,
    x_list,
    x_options,
    y_list,
    y_options,
    width,
    height
):
    start_x = 25
    start_y = 25

    attributes = dict()

    col = (position.x - start_x) / width - len(y_list)
    for attr in reversed(x_list):
        opt = col % len(x_options[attr])
        attributes[attr] = x_options[attr][int(opt)]

        col /= len(x_options[attr])
    row = (position.y - start_y) / height - len(x_list)
    for attr in reversed(y_list):
        opt = row % len(y_options[attr])
        attributes[attr] = y_options[attr][int(opt)]

        row /= len(y_options[attr])

    return attributes


CARD_TEXT_PREFIX = 'card_text'
CARD_NOTE_PREFIX = 'card_note'

_WIDTH = 50


def create_card_object(
    canvas: tkinter.Canvas,
    obj: internal.objects.interfaces.IBoardObjectCard,
    coordinates: (int, int)
) -> int:
    text_tag = f'{CARD_TEXT_PREFIX}{obj.id}'
    note_tag = f'{CARD_NOTE_PREFIX}{obj.id}'
    canvas.create_text(
        coordinates[0],
        coordinates[1],
        text=obj.text,
        fill=obj.font.color,
        tags=[obj.id, text_tag],
        width=_WIDTH,
        font=(obj.font.family, int(obj.font.size), obj.font.weight, obj.font.slant)
    )

    arr = create_note_coord(canvas, obj.id, _WIDTH)
    canvas.create_rectangle(
        arr,
        fill=obj.color,
        tags=[obj.id, note_tag],
    )
    canvas.tag_lower(note_tag, text_tag)
    adjust_font(canvas, obj)


def create_note_coord(
    canvas: tkinter.Canvas,
    obj_id: internal.objects.interfaces.ObjectId,
    width: int
):
    args = canvas.bbox(obj_id)
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
    canvas: tkinter.Canvas,
    obj: internal.objects.interfaces.IBoardObjectCard,
    larger=True
):
    text_tag = f'{CARD_TEXT_PREFIX}{obj.id}'
    width = int(canvas.itemcget(text_tag, 'width'))
    _, y1, _, y2 = canvas.bbox(text_tag)
    floated_size = float(obj.font.size)
    if larger:
        while abs(y1 - y2) > width:
            floated_size /= 1.05
            canvas.itemconfig(text_tag, font=_get_font(obj))
            _, y1, _, y2 = canvas.bbox(text_tag)
    else:
        while abs(y1 - y2) < width * 0.7:
            floated_size *= 1.05
            canvas.itemconfig(text_tag, font=_get_font(obj))
            _, y1, _, y2 = canvas.bbox(text_tag)
            y1 = canvas.canvasx(y1)
            y2 = canvas.canvasy(y2)
