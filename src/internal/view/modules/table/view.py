import copy

import internal.objects.interfaces
import internal.view.dependencies


# TODO function for tags
def create_table_object(
        dependencies: internal.view.dependencies.Dependencies,
        obj: internal.objects.interfaces.IBoardObjectTable
) -> None:
    cells = [[dependencies.canvas.create_rectangle(obj.position.x + sum(obj.columns_width[:i]),
                                                   obj.position.y + sum(obj.rows_height[:j]),
                                                   obj.position.x + sum(obj.columns_width[:i + 1]),
                                                   obj.position.y + sum(obj.rows_height[:j + 1]),
                                                   fill='white',
                                                   tag=[obj.id, f"{i},{j}/" + obj.id, "table", "table" + obj.id])
              for i in range(obj.columns)] for j in range(obj.rows)]

    add_c = dependencies.canvas.create_text(obj.position.x + sum(obj.columns_width) + 10, obj.position.y,
                                            text="+", tags=[obj.id, obj.id + 'add_c'])

    add_r = dependencies.canvas.create_text(obj.position.x + sum(obj.columns_width) / 2,
                                            obj.position.y + sum(obj.rows_height) + 10,
                                            text="+", tags=[obj.id, obj.id + 'add_r'])

    column_lines = [dependencies.canvas.create_line(obj.position.x + sum(obj.columns_width[:i]), obj.position.y,
                                                    obj.position.x + sum(obj.columns_width[:i]),
                                                    obj.position.y + sum(obj.rows_height),
                                                    tags=[obj.id, obj.id + 'col_l', 'line', f'{i - 1}',
                                                          obj.id + 'col_l' + f'/{i - 1}']) for i in
                    range(1, obj.columns + 1)]

    row_lines = [dependencies.canvas.create_line(obj.position.x, obj.position.y + sum(obj.rows_height[:i]),
                                                 obj.position.x + sum(obj.columns_width),
                                                 obj.position.y + sum(obj.rows_height[:i]),
                                                 tags=[obj.id, obj.id + 'row_l', 'line', f'{i - 1}',
                                                       obj.id + 'row_l' + f'/{i - 1}']) for i in
                 range(1, obj.rows + 1)]
    # return [cells, add_c, add_r, column_lines, row_lines]


def add_column(
        dependencies: internal.view.dependencies.Dependencies,
        obj: internal.objects.interfaces.IBoardObjectTable
) -> (list, list):
    _, _, edge_x, edge_y = dependencies.canvas.coords(f"{obj.columns - 1},{obj.rows - 1}/" + obj.id)
    for j in range(obj.rows):
        _, y1, _, y2 = dependencies.canvas.coords(f"{obj.columns - 1},{j}/" + obj.id)
        dependencies.canvas.create_rectangle(edge_x, y1,
                                             edge_x + obj.default_width,
                                             y2,
                                             fill='white',
                                             tags=[obj.id, f"{obj.columns},{j}/" + obj.id, "table",
                                                   "table" + obj.id])
    i = obj.columns

    _, y1, _, y2 = dependencies.canvas.coords(obj.id + 'col_l' + f'/{i - 1}')
    dependencies.canvas.create_line(edge_x + obj.default_width, y1,
                                    edge_x + obj.default_width,
                                    y2,
                                    tags=[obj.id, obj.id + 'col_l', 'line', f'{i}',
                                          obj.id + 'col_l' + f'/{i}'])
    for row in range(obj.rows):
        x1, y1, x2, y2 = dependencies.canvas.coords(obj.id + 'row_l' + f'/{row}')
        dependencies.canvas.coords(obj.id + 'row_l' + f'/{row}', x1, y1, x2 + obj.default_width, y2)
    dependencies.canvas.move(obj.id + 'add_c', obj.default_width, 0)
    dependencies.canvas.move(obj.id + 'add_r', obj.default_width * 1.0 / 2, 0)
    dependencies.canvas.tag_lower(obj.id)
    dependencies.canvas.tag_lower("table" + obj.id)

    return obj.columns_width + [obj.default_width], obj.rows_height


def add_row(
        dependencies: internal.view.dependencies.Dependencies,
        obj: internal.objects.interfaces.IBoardObjectTable
) -> (list, list):
    _, _, edge_x, edge_y = dependencies.canvas.coords(f"{obj.columns - 1},{obj.rows - 1}/" + obj.id)

    for i in range(obj.columns):
        x1, _, x2, _ = dependencies.canvas.coords(f"{i},{obj.rows - 1}/" + obj.id)
        dependencies.canvas.create_rectangle(x1, edge_y,
                                             x2,
                                             edge_y + obj.default_height,
                                             fill='white',
                                             tags=[obj.id, f"{i},{obj.rows}/" + obj.id, "table",
                                                   "table" + obj.id])

    i = obj.rows

    x1, _, x2, _ = dependencies.canvas.coords(obj.id + 'row_l' + f'/{i - 1}')

    dependencies.canvas.create_line(x1, edge_y + obj.default_height,
                                    x2,
                                    edge_y + obj.default_height,
                                    tags=[obj.id, obj.id + 'row_l', 'line', f'{i}',
                                          obj.id + 'row_l' + f'/{i}'])
    for col in range(obj.columns):
        x1, y1, x2, y2 = dependencies.canvas.coords(obj.id + 'col_l' + f'/{col}')
        dependencies.canvas.coords(obj.id + 'col_l' + f'/{col}', x1, y1, x2, y2 + obj.default_height)

    dependencies.canvas.tag_lower(obj.id)
    dependencies.canvas.tag_lower("table" + obj.id)
    dependencies.canvas.move(obj.id + 'add_r', 0, obj.default_height)
    return obj.columns_width, obj.rows_height + [obj.default_height]


def resize_column(
        dependencies: internal.view.dependencies.Dependencies,
        obj: internal.objects.interfaces.IBoardObjectTable,
        column,
        x  # current position
) -> (list, list):
    x1, y1, x2, y2 = dependencies.canvas.coords(obj.id + 'col_l' + f'/{column}')

    delta = x - x2
    dependencies.canvas.move(obj.id + 'add_c', delta, 0)

    for col in range(column, obj.columns):
        dependencies.canvas.move(obj.id + 'col_l' + f'/{col}', delta, 0)

    for row in range(obj.rows):
        x1, y1, x2, y2 = dependencies.canvas.coords(obj.id + 'row_l' + f'/{row}')
        dependencies.canvas.coords(obj.id + 'row_l' + f'/{row}', x1, y1, x2 + delta, y2)

    for i in range(obj.rows):
        x1, y1, x2, y2 = dependencies.canvas.coords(f"{column},{i}/" + obj.id)
        dependencies.canvas.coords(f"{column},{i}/" + obj.id, x1, y1, x, y2)

        for col in range(column + 1, obj.columns):
            dependencies.canvas.move(f"{col},{i}/" + obj.id, delta, 0)

    temp = copy.deepcopy(obj.columns_width)
    temp[column] = x2 - x1
    return temp, obj.rows_height
    # TODO обработка элементов внутри
    # move objects inside
    # for i in range(c + 1, obj.rows):
    #     for j in range(0, obj.columns):
    #         dependencies.canvas.move(obj.tags_object(f"{j},{i}"), diff, 0)


def resize_row(
        dependencies: internal.view.dependencies.Dependencies,
        obj: internal.objects.interfaces.IBoardObjectTable,
        row_n,
        y
) -> (list, list):
    x1, y1, x2, y2 = dependencies.canvas.coords(obj.id + 'row_l' + f'/{row_n}')

    diff = y - y2
    dependencies.canvas.move(obj.id + 'add_r', 0, diff)
    for row in range(row_n, obj.rows):
        dependencies.canvas.move(obj.id + 'row_l' + f'/{row}', 0, diff)
    for col in range(obj.columns):
        x1, y1, x2, y2 = dependencies.canvas.coords(obj.id + 'col_l' + f'/{col}')
        dependencies.canvas.coords(obj.id + 'col_l' + f'/{col}', x1, y1, x2, y2 + diff)

    for col in range(obj.columns):
        x1, y1, x2, y2 = dependencies.canvas.coords(f"{col},{row_n}/" + obj.id)
        # diff = x - y2
        dependencies.canvas.coords(f"{col},{row_n}/" + obj.id, x1, y1, x2, y)
    for j in range(row_n + 1, obj.rows):
        for col in range(obj.columns):
            dependencies.canvas.move(f"{col},{j}/" + obj.id, 0, diff)
    # self.move_inside(0, r + 1, 0, diff)

    temp = copy.deepcopy(obj.rows_height)
    temp[row_n] = y2 - y1
    return obj.columns_width, temp



# TODO adjust cells to the object
