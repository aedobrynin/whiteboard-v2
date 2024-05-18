from __future__ import annotations

import tkinter
import tkinter.font
import tkinter.ttk
from typing import List, Callable, Iterable, Tuple

import internal.objects.events
import internal.objects.interfaces
import internal.repositories.events
import internal.repositories.interfaces
import internal.view.dependencies
import internal.view.objects.interfaces
from internal.view.objects.impl.object import ViewObject
from internal.view.utils import (
    get_line_widths,
    get_font_colors,
    get_connector_types,
    get_stroke_styles
)

_LINE_WIDTH_DESC = 'Толщина линии'
_LINE_COLOR_DESC = 'Цвет линии'
_CONNECTOR_TYPE_DESC = 'Тип линии'
_STROKE_STYLE_DESC = 'Тип связи'


class ConnectorObject(ViewObject):
    def __init__(
        self,
        dependencies: internal.view.dependencies.Dependencies,
        obj: internal.objects.interfaces.IBoardObjectConnector
    ):
        ViewObject.__init__(self, obj)
        self._line_id = None
        self._start_id = obj.start_id
        self._end_id = obj.end_id
        self._connector_type = obj.connector_type
        self._stroke_style = obj.stroke_style
        self.curve(dependencies)

        self._subscribe_to_repo_object_events(dependencies)
        # TODO: because notifications came after move-done, connector doesnt redraw properly
        dependencies.canvas.addtag_withtag(obj.id, obj.start_id)
        dependencies.canvas.addtag_withtag(obj.id, obj.end_id)

    @property
    def line_id(self):
        return self._line_id

    @property
    def start_id(self):
        return self._start_id

    @property
    def end_id(self):
        return self._end_id

    def curve(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        points = self._get_points(dependencies)
        if self._connector_type == 'straight':
            points = self._extend_points([points[0], points[-1]])
        elif self._connector_type == 'elbowed':
            points = self._extend_points(points)
        else:
            points = self._extend_points(self._find_basic_points_of_bezier(points))
        if self.line_id:
            dependencies.canvas.coords(self.line_id, points)
        else:
            obj: internal.objects.interfaces.IBoardObjectConnector = dependencies.repo.get(
                self.id
            )
            self._line_id = dependencies.canvas.create_line(
                points, width=obj.width, tags=[obj.id], fill=obj.color, arrow=obj.stroke_style
            )

    def _get_points(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        xs1, ys1, xs2, ys2 = dependencies.canvas.bbox(self.start_id)
        xe1, ye1, xe2, ye2 = dependencies.canvas.bbox(self.end_id)
        points = []
        if xs2 < xe1 and ys2 < ye1:
            # point 1
            points.append(((xs1 + xs2) / 2, ys2))
            # point 2
            points.append(((xs1 + xs2) / 2, (ye1 + ye2) / 2))
            # point 3
            points.append((xe1, (ye1 + ye2) / 2))
        elif xs1 >= xe2 and (ye1 <= ys1 <= ye2 or ye1 <= ys2 <= ye2):
            # point 1
            points.append((xs1, (ys1 + ys2) / 2))
            # point 2
            points.append(((xs1 + xe2) / 2, (ys1 + ys2) / 2))
            # point 3
            points.append(((xs1 + xe2) / 2, (ye1 + ye2) / 2))
            # point 4
            points.append((xe2, (ye1 + ye2) / 2))
        elif xe1 >= xs2 and (ye1 <= ys1 <= ye2 or ye1 <= ys2 <= ye2):
            # point 1
            points.append((xs2, (ys1 + ys2) / 2))
            # point 2
            points.append(((xs2 + xe1) / 2, (ys1 + ys2) / 2))
            # point 3
            points.append(((xs2 + xe1) / 2, (ye1 + ye2) / 2))
            # point 4
            points.append((xe1, (ye1 + ye2) / 2))
        elif xs1 <= xe1 < xs2 and ys2 < ye1:
            # point 1
            points.append(((xs1 + xs2) / 2, ys2))
            # point 2
            points.append(((xs1 + xs2) / 2, (ye1 + ys2) / 2))
            # point 3
            points.append(((xe1 + xe2) / 2, (ye1 + ys2) / 2))
            # point 4
            points.append(((xe1 + xe2) / 2, ye1))
        elif xe1 <= xs1 < xe2 and ys2 < ye1:
            # point 1
            points.append(((xs1 + xs2) / 2, ys2))
            # point 2
            points.append(((xs1 + xs2) / 2, (ye1 + ys2) / 2))
            # point 3
            points.append(((xe1 + xe2) / 2, (ye1 + ys2) / 2))
            # point 4
            points.append(((xe1 + xe2) / 2, ye1))
        elif xs1 <= (xe1 + xe2) / 2 <= xs2 and ys2 < ye1:
            # point 1
            points.append(((xs1 + xs2) / 2, ys2))
            # point 2
            points.append(((xs1 + xs2) / 2, (ye1 + ys2) / 2))
            # point 3
            points.append(((xe1 + xe2) / 2, (ye1 + ys2) / 2))
            # point 4
            points.append(((xe1 + xe2) / 2, ye1))
        elif xs1 >= xe2 and ys2 < ye2:
            # point 1
            points.append(((xs1 + xs2) / 2, ys2))
            # point 2
            points.append(((xs1 + xs2) / 2, (ye1 + ye2) / 2))
            # point 3
            points.append((xe2, (ye1 + ye2) / 2))
        elif xs2 < xe1 and ys1 > ye2:
            # point 1
            points.append(((xs1 + xs2) / 2, ys1))
            # point 2
            points.append(((xs1 + xs2) / 2, (ye1 + ye2) / 2))
            # point 3
            points.append((xe1, (ye1 + ye2) / 2))
        elif xs1 <= xe1 < xs2 and ys1 > ye2:
            # point 1
            points.append(((xs1 + xs2) / 2, ys1))
            # point 2
            points.append(((xs1 + xs2) / 2, (ye2 + ys1) / 2))
            # point 3
            points.append(((xe1 + xe2) / 2, (ye2 + ys1) / 2))
            # point 4
            points.append(((xe1 + xe2) / 2, ye2))
        elif xe1 <= xs1 <= xe2 and ys1 > ye2:
            # point 1
            points.append(((xs1 + xs2) / 2, ys1))
            # point 2
            points.append(((xs1 + xs2) / 2, (ye2 + ys1) / 2))
            # point 3
            points.append(((xe1 + xe2) / 2, (ye2 + ys1) / 2))
            # point 4
            points.append(((xe1 + xe2) / 2, ye2))
        elif xs1 >= xe2 and ys1 > ye2:
            # point 1
            points.append(((xs1 + xs2) / 2, ys1))
            # point 2
            points.append(((xs1 + xs2) / 2, (ye1 + ye2) / 2))
            # point 3
            points.append((xe2, (ye1 + ye2) / 2))
        else:
            # point 1
            points.append((xs1, (ys1 + ys2) / 2))
            # point 2
            points.append(((xs1 + xe2) / 2, (ys1 + ys2) / 2))
            # point 3
            points.append(((xs1 + xe2) / 2, (ye1 + ye1) / 2))
            # point 4
            points.append(((xe1 + xe2) / 2, (ye1 + ye1) / 2))
        return points

    def _find_basic_points_of_bezier(
        self, elbowed_points: List[Tuple[int, int]]
    ):
        basic_p = elbowed_points
        points_cnt = 10
        points = []
        if len(basic_p) > 2:
            for i in range(points_cnt):
                t = i / (points_cnt - 1)
                x, y = self._bezier(t, *basic_p)
                points.append((x, y))
        else:
            points = basic_p
        return points

    def _subscribe_to_repo_object_events(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        dependencies.pub_sub_broker.subscribe(
            self.id, internal.repositories.interfaces.REPOSITORY_PUB_SUB_ID,
            internal.repositories.events.EVENT_TYPE_OBJECT_DELETED,
            lambda publisher, event, repo: self._destroy_by_end(dependencies, event)
        )
        dependencies.pub_sub_broker.subscribe(
            self.id, self.start_id,
            internal.objects.events.EVENT_TYPE_OBJECT_MOVED,
            lambda publisher, event, repo: self.curve(dependencies)
        )
        dependencies.pub_sub_broker.subscribe(
            self.id, self.end_id,
            internal.objects.events.EVENT_TYPE_OBJECT_MOVED,
            lambda publisher, event, repo: self.curve(dependencies)
        )
        dependencies.pub_sub_broker.subscribe(
            self.id, self.start_id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_SIZE,
            lambda publisher, event, repo: self.curve(dependencies)
        )
        dependencies.pub_sub_broker.subscribe(
            self.id, self.end_id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_SIZE,
            lambda publisher, event, repo: self.curve(dependencies)
        )
        dependencies.pub_sub_broker.subscribe(
            self.id, self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_COLOR,
            lambda publisher, event, repo: self._get_color_update_from_repo(dependencies),
        )
        dependencies.pub_sub_broker.subscribe(
            self.id, self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_WIDTH,
            lambda publisher, event, repo: self._get_width_update_from_repo(dependencies),
        )
        dependencies.pub_sub_broker.subscribe(
            self.id, self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_CONNECTOR_TYPE,
            lambda publisher, event, repo: self._get_con_type_update_from_repo(dependencies)
        )
        dependencies.pub_sub_broker.subscribe(
            self.id, self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_STROKE_STYLE,
            lambda publisher, event, repo: self._get_stroke_update_from_repo(dependencies)
        )

    def _unsubscribe_from_repo_object_events(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        # TODO: Issue 47
        #  we cannot call unsubscribe when we are in process of published DELETE_OBJECT
        # dependencies.pub_sub_broker.unsubscribe_from_all(self.id)
        # dependencies.pub_sub_broker.unsubscribe(
        #     self.id, internal.repositories.interfaces.REPOSITORY_PUB_SUB_ID
        # )
        dependencies.pub_sub_broker.unsubscribe(self.id, self.start_id)
        dependencies.pub_sub_broker.unsubscribe(self.id, self.end_id)
        dependencies.pub_sub_broker.unsubscribe(self.id, self.id)

    def _destroy_by_end(
        self, dependencies: internal.view.dependencies.Dependencies,
        event: internal.repositories.events.EventObjectDeleted
    ):
        if self.start_id != event.object_id and self.end_id != event.object_id:
            return
        if dependencies.repo.get(self.id):
            dependencies.controller.delete_object(self.id)

    def destroy(self, dependencies: internal.view.dependencies.Dependencies):
        dependencies.canvas.dtag(self.start_id, self.id)
        dependencies.canvas.dtag(self.end_id, self.id)
        self._unsubscribe_from_repo_object_events(dependencies)
        dependencies.canvas.delete(self.id)

    def _get_color_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectPen = dependencies.repo.get(self.id)
        dependencies.canvas.itemconfigure(self.line_id, fill=obj.color)

    def _get_width_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectPen = dependencies.repo.get(self.id)
        dependencies.canvas.itemconfigure(self.line_id, width=obj.width)

    def _get_con_type_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectConnector = dependencies.repo.get(self.id)
        self._connector_type = obj.connector_type
        self.curve(dependencies)

    def _get_stroke_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectConnector = dependencies.repo.get(self.id)
        self._stroke_style = obj.stroke_style
        dependencies.canvas.itemconfigure(self.line_id, arrow=self._stroke_style)

    def widgets(
        self, dependencies: internal.view.dependencies.Dependencies
    ) -> List[tkinter.ttk.Widget]:
        _widgets = []
        for func in self._widgets_func():
            label, combobox = func(dependencies)
            _widgets.append(label)
            _widgets.append(combobox)
        return _widgets

    def _widgets_func(self) -> List[Callable]:
        return [
            lambda dependencies: self._base_widget(
                dependencies,
                get_font_colors(),
                _LINE_COLOR_DESC,
                self.get_color,
                self.set_color
            ),
            lambda dependencies: self._base_widget(
                dependencies,
                get_line_widths(),
                _LINE_WIDTH_DESC,
                self.get_width,
                self.set_width
            ),
            lambda dependencies: self._base_widget(
                dependencies,
                get_connector_types(),
                _CONNECTOR_TYPE_DESC,
                self.get_connector_type,
                self.set_connector_type
            ),
            lambda dependencies: self._base_widget(
                dependencies,
                get_stroke_styles(),
                _STROKE_STYLE_DESC,
                self.get_stroke_style,
                self.set_stroke_style
            )
        ]

    def _base_widget(
        self,
        dependencies: internal.view.dependencies.Dependencies,
        restrictions: List,
        description: str,
        getter: Callable,
        setter: Callable
    ) -> List[tkinter.ttk.Widget]:
        string_var = tkinter.StringVar()
        label = tkinter.ttk.Label(
            dependencies.property_bar,
            text=description,
            justify='left',
            anchor='w'
        )
        combobox = tkinter.ttk.Combobox(
            dependencies.property_bar,
            textvariable=string_var,
            values=restrictions,
            state='readonly'
        )
        combobox.current(restrictions.index(getter(
            dependencies
        )))
        string_var.trace('w', lambda *_: setter(
            dependencies, string_var.get()
        ))
        return [label, combobox]

    def get_color(self, dependencies: internal.view.dependencies.Dependencies):
        return dependencies.canvas.itemcget(self.line_id, 'fill')

    def set_color(self, dependencies: internal.view.dependencies.Dependencies, color: str):
        dependencies.controller.edit_color(self.id, color=color)

    def get_width(self, dependencies: internal.view.dependencies.Dependencies):
        return int(float(dependencies.canvas.itemcget(self.line_id, 'width')))

    def set_width(self, dependencies: internal.view.dependencies.Dependencies, width: int):
        dependencies.controller.edit_width(self.id, width=width)

    def get_connector_type(self, dependencies: internal.view.dependencies.Dependencies):
        return self._connector_type

    def set_connector_type(
        self, dependencies: internal.view.dependencies.Dependencies, connector_type: str
    ):
        dependencies.controller.edit_connector_type(self.id, connector_type=connector_type)

    def get_stroke_style(self, dependencies: internal.view.dependencies.Dependencies):
        return self._stroke_style

    def set_stroke_style(
        self, dependencies: internal.view.dependencies.Dependencies, stroke_style: str
    ):
        dependencies.controller.edit_stroke_style(self.id, stroke_style=stroke_style)

    @staticmethod
    def _bezier(t, *points):
        c = []
        cnt = len(points)
        if cnt == 3:
            c += [1, 2, 1]
        if cnt == 4:
            c += [1, 3, 3, 1]
        x = sum(c[i] * (1 - t) ** (cnt - 1 - i) * t ** i * points[i][0] for i in range(cnt))
        y = sum(c[i] * (1 - t) ** (cnt - 1 - i) * t ** i * points[i][1] for i in range(cnt))
        return x, y

    @staticmethod
    def _extend_points(points: Iterable[int or float]):
        extended = []
        for point in points:
            extended.extend(point)
        return extended
