import copy
import re
import logging
import tkinter.ttk
from typing import List, Optional

import internal.controller
import internal.models
import internal.objects.interfaces
import internal.objects.events
import internal.repositories.interfaces
import internal.repositories.events
import internal.view.dependencies
import internal.view.objects.interfaces
import internal.view.utils
from internal.view.objects.impl.object import ViewObject


class TableObject(ViewObject):
    _cells: list
    _add_column_id: int
    _add_row_id: int
    _column_lines: int
    _row_lines: int

    def __init__(
        self,
        dependencies: internal.view.dependencies.Dependencies,
        obj: internal.objects.interfaces.IBoardObjectTable,
    ):
        ViewObject.__init__(self, obj)
        self.draw_table(dependencies)
        self._subscribe_to_repo_object_events(dependencies)
        dependencies.canvas.tag_lower(self.id)

    @property
    def add_column_id(self):
        return self._add_column_id

    @property
    def add_row_id(self):
        return self._add_row_id

    @property
    def column_lines(self):
        return self._column_lines

    @property
    def row_lines(self):
        return self._row_lines

    @property
    def cells(self):
        return self._cells

    # TODO: очень много легаси, нужно поправить
    def draw_table(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectTable = dependencies.repo.get(self.id)
        position = internal.models.Position(
            obj.position.x * dependencies.scaler,
            obj.position.y * dependencies.scaler,
            obj.position.z
        )
        if not obj:
            logging.warning('Table object not found')
            return
        self._cells = [[
            dependencies.canvas.create_rectangle(
                position.x + sum(obj.columns_width[:i]),
                position.y + sum(obj.rows_height[:j]),
                position.x + sum(obj.columns_width[:i + 1]),
                position.y + sum(obj.rows_height[:j + 1]),
                fill='white',
                tags=[obj.id, f'{i},{j}/' + obj.id, 'table', 'table' + obj.id]
            )
            for i in range(obj.columns)
        ] for j in range(obj.rows)]

        self._add_column_id = dependencies.canvas.create_text(
            position.x + sum(obj.columns_width) + 10, position.y, text='+',
            tags=[obj.id]
        )

        self._add_row_id = dependencies.canvas.create_text(
            position.x + sum(obj.columns_width) / 2, position.y + sum(obj.rows_height) + 10,
            text='+', tags=[obj.id]
        )

        self._column_lines = [
            dependencies.canvas.create_line(
                position.x + sum(obj.columns_width[:i]),
                position.y,
                position.x + sum(obj.columns_width[:i]),
                position.y + sum(obj.rows_height),
                tags=[obj.id, obj.id + 'col_l', 'line', f'{i - 1}', obj.id + 'col_l' + f'/{i - 1}']
            ) for i in range(1, obj.columns + 1)
        ]

        self._row_lines = [
            dependencies.canvas.create_line(
                position.x,
                position.y + sum(obj.rows_height[:i]),
                position.x + sum(obj.columns_width),
                position.y + sum(obj.rows_height[:i]),
                tags=[obj.id, obj.id + 'row_l', 'line', f'{i - 1}',
                      obj.id + 'row_l' + f'/{i - 1}']
            ) for i in range(1, obj.rows + 1)
        ]
        dependencies.canvas.tag_lower(self.id)

    def _subscribe_to_repo_object_events(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        dependencies.pub_sub_broker.subscribe(
            self.id, self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_MOVED,
            lambda publisher, event, repo: (
                self._get_move_update_from_repo(dependencies)
            )
        )

        dependencies.pub_sub_broker.subscribe(
            self.id, self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_SIZE,
            lambda publisher, event, repo: (
                self._get_update_columns_and_rows_from_repo(dependencies)
            )
        )
        dependencies.pub_sub_broker.subscribe(
            self.id, self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_LINKED_OBJECTS,
            lambda publisher, event, repo: (
                self._get_linked_objects_update_from_repo(dependencies)
            )
        )
        self._get_linked_objects_update_from_repo(dependencies)

    def _get_linked_objects_update_from_repo(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        obj: internal.objects.interfaces.IBoardObjectTable = dependencies.repo.get(self.id)
        for child_id in obj.linked_objects:
            dependencies.pub_sub_broker.subscribe(
                self.id, child_id,
                internal.objects.events.EVENT_TYPE_OBJECT_MOVED,
                lambda publisher, event, repo: self._get_child_move_update(dependencies, event)
            )
            dependencies.pub_sub_broker.subscribe(
                self.id, child_id,
                internal.repositories.events.EVENT_TYPE_OBJECT_DELETED,
                lambda publisher, event, repo: self._get_child_remove_update(dependencies, event)
            )

    def _get_move_update_from_repo(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        obj: internal.objects.interfaces.IBoardObjectTable = dependencies.repo.get(self.id)
        position = internal.models.Position(
            obj.position.x * dependencies.scaler,
            obj.position.y * dependencies.scaler,
            obj.position.z
        )
        dependencies.canvas.moveto(obj.id, position.x, position.y)

    def _get_child_move_update(
        self, dependencies: internal.view.dependencies.Dependencies,
        event: internal.objects.events.EventObjectMoved
    ):
        obj: internal.objects.interfaces.IBoardObjectTable = dependencies.repo.get(self.id)
        if event.object_id not in obj.linked_objects:
            return
        coord = obj.linked_objects[event.object_id]
        x1, y1, x2, y2 = dependencies.canvas.coords(f"{int(coord[0])},{int(coord[1])}/" + self.id)
        # we check current position on canvas
        x_obj_1, y_obj_1, x_obj_2, y_obj_2 = dependencies.canvas.bbox(event.object_id)
        if x_obj_2 > x2 or x_obj_1 < x1 or y_obj_2 > y2 or y_obj_1 < y1:
            linked_obj: dict[str, list] = dict()
            for child_id, coord in obj.linked_objects.items():
                if child_id != event.object_id:
                    linked_obj[child_id] = coord
            dependencies.controller.edit_linked_objects(self.id, linked_obj=linked_obj)

    def _get_child_remove_update(
        self, dependencies: internal.view.dependencies.Dependencies,
        event: internal.objects.events.EventObjectMoved
    ):
        obj: internal.objects.interfaces.IBoardObjectTable = dependencies.repo.get(self.id)
        if event.object_id not in obj.linked_objects:
            return
        dependencies.pub_sub_broker.unsubscribe(self.id, event.object_id)
        linked_obj: dict[str, list] = dict()
        for child_id, coord in obj.linked_objects.items():
            if child_id != event.object_id:
                linked_obj[child_id] = coord
        dependencies.controller.edit_linked_objects(self.id, linked_obj=linked_obj)

    def _get_update_columns_and_rows_from_repo(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        obj: internal.objects.interfaces.IBoardObjectTable = dependencies.repo.get(self.id)
        if not obj:
            logging.warning('Table object not found')
            return
        # TODO: now we delete all table and redraw, it`s bad practice
        dependencies.canvas.delete(self.id)
        self.draw_table(dependencies)

    def resize_column(
        self, dependencies: internal.view.dependencies.Dependencies, column, x  # current position
    ) -> (list, list):
        obj: internal.objects.interfaces.IBoardObjectTable = dependencies.repo.get(self.id)
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

        dependencies.canvas.move(self.add_column_id, delta, 0)

        temp = copy.deepcopy(obj.columns_width)
        temp[column] = x2 - x1
        return temp, obj.rows_height

    def resize_row(
        self, dependencies: internal.view.dependencies.Dependencies, row_n, y
    ) -> (list, list):
        obj: internal.objects.interfaces.IBoardObjectTable = dependencies.repo.get(self.id)
        x1, y1, x2, y2 = dependencies.canvas.coords(self.id + 'row_l' + f'/{row_n}')

        diff = y - y2
        dependencies.canvas.move(self.id + 'add_r', 0, diff)
        for row in range(row_n, obj.rows):
            dependencies.canvas.move(self.id + 'row_l' + f'/{row}', 0, diff)
        for col in range(obj.columns):
            x1, y1, x2, y2 = dependencies.canvas.coords(self.id + 'col_l' + f'/{col}')
            dependencies.canvas.coords(self.id + 'col_l' + f'/{col}', x1, y1, x2, y2 + diff)

        for col in range(obj.columns):
            x1, y1, x2, y2 = dependencies.canvas.coords(f"{col},{row_n}/" + self.id)
            dependencies.canvas.coords(f"{col},{row_n}/" + self.id, x1, y1, x2, y)
        for j in range(row_n + 1, obj.rows):
            for col in range(obj.columns):
                dependencies.canvas.move(f"{col},{j}/" + self.id, 0, diff)

        dependencies.canvas.move(self.add_row_id, 0, diff)
        temp = copy.deepcopy(obj.rows_height)
        temp[row_n] = y2 - y1
        return obj.columns_width, temp

    @staticmethod
    def add_object(
        dependencies: internal.view.dependencies.Dependencies, position: internal.models.Position
    ) -> (Optional[internal.objects.interfaces.ObjectId], list):
        # TODO think about the type
        x = position.x
        y = position.y
        overlap = list(dependencies.canvas.find_overlapping(x, y, x, y))
        for widget_id in overlap:
            tags = dependencies.canvas.gettags(widget_id)
            if 'table' in tags:
                ids = [s for s in tags if re.search('[0-9]+,[0-9]+', s)]
                cell, obj_id = ids[0].split('/')
                x, y = map(lambda c: int(c), cell.split(','))
                if ids:
                    return tags[0], [x, y]
                break
        return None, [None, None]

    def _unsubscribe_from_repo_object_events(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        dependencies.pub_sub_broker.unsubscribe(self.id, self.id)

    def widgets(
        self, dependencies: internal.view.dependencies.Dependencies
    ) -> List[tkinter.ttk.Widget]:
        return []
