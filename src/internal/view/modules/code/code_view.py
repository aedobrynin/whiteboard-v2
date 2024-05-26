from __future__ import annotations

import tkinter
import tkinter.font
import tkinter.ttk
from pygments import lex
from pygments.lexers import PythonLexer, PostgresLexer, JavaLexer

from typing import List, Callable

import internal.objects.interfaces
import internal.objects.events
import internal.repositories.interfaces
import internal.view.dependencies
import internal.view.objects.interfaces
from internal.view.objects.impl.object import ViewObject
from internal.view.consts import VIEW_OBJECT_ID
import internal.view.utils

_FONT_SIZE_DESC = 'Размер шрифта'
_LEXER_DESC = 'Язык'
_DEFAULT_WIDTH = 100
_DEFAULT_HEIGHT = 100
_DEFAULT_COLOR = 'gray'


class CodeObject(ViewObject):
    def __init__(
        self,
        dependencies: internal.view.dependencies.Dependencies,
        obj: internal.objects.interfaces.IBoardObjectCode,
    ):
        ViewObject.__init__(self, obj)
        self._text = tkinter.Text(
            dependencies.canvas,
            width=_DEFAULT_WIDTH,
            height=_DEFAULT_HEIGHT,
            wrap='word',
            bd=0,
            font=(obj.font.family, int(obj.font.size), obj.font.weight, obj.font.slant)
        )
        self._rectangle_id = dependencies.canvas.create_rectangle(
            obj.position.x, obj.position.y,
            obj.position.x + _DEFAULT_WIDTH, obj.position.y + _DEFAULT_HEIGHT,
            tags=[self.id], fill=_DEFAULT_COLOR,  # do not remove
            stipple='@internal/view/modules/code/xbms/transparent.xbm',
        )
        self._window_id = dependencies.canvas.create_window(
            obj.position.x + _DEFAULT_WIDTH / 2, obj.position.y + _DEFAULT_HEIGHT / 2,
            window=self.text, tags=[self.id], width=_DEFAULT_WIDTH, height=_DEFAULT_HEIGHT
        )
        self.text.insert(tkinter.END, obj.text)
        self._lexer = obj.lexer
        self._text_tag_configure()
        self._subscribe_to_repo_object_events(dependencies)
        self._lexer_map = {
            'python': PythonLexer(),
            'sql': PostgresLexer(),
            'java': JavaLexer()
        }
        self.highlight()
        dependencies.canvas.tag_lower(self.window_id, self.rectangle_id)

    @property
    def window_id(self):
        return self._window_id

    @property
    def rectangle_id(self):
        return self._rectangle_id

    @property
    def text(self) -> tkinter.Text:
        return self._text

    def set_focused(self, dependencies: internal.view.dependencies.Dependencies, is_focus: bool):
        super().set_focused(dependencies, is_focus)
        if is_focus:
            dependencies.canvas.tag_lower(self.rectangle_id, self.window_id)
        else:
            dependencies.canvas.tag_lower(self.window_id, self.rectangle_id)

    def highlight(self):
        data = self.text.get("1.0", tkinter.END)
        self.text.mark_set("range_start", "0.0")
        for token, content in lex(data, self._lexer_map[self._lexer]):
            self.text.mark_set("range_end", "range_start+%dc" % len(content))
            self.text.tag_add(str(token), "range_start", "range_end")
            self.text.mark_set("range_start", "range_end")

    def _text_tag_configure(self):
        self.text.tag_configure("Token.Name.Builtin", foreground="#003D99")
        self.text.tag_configure("Token.Literal.String.Single", foreground="#008000")
        self.text.tag_configure("Token.Literal.String.Double", foreground="#008000")
        self.text.tag_configure("Token.Keyword", foreground="#CC7A00")
        self.text.tag_configure("Token.Keyword.Constant", foreground="#CC7A00")
        self.text.tag_configure("Token.Keyword.Declaration", foreground="#CC7A00")
        self.text.tag_configure("Token.Keyword.Namespace", foreground="#CC7A00")
        self.text.tag_configure("Token.Keyword.Pseudo", foreground="#CC7A00")
        self.text.tag_configure("Token.Keyword.Reserved", foreground="#CC7A00")
        self.text.tag_configure("Token.Keyword.Type", foreground="#CC7A00")
        self.text.tag_configure("Token.Name.Class", foreground="#003D99")
        self.text.tag_configure("Token.Name.Exception", foreground="#003D99")
        self.text.tag_configure("Token.Name.Function", foreground="#003D99")
        self.text.tag_configure("Token.Operator.Word", foreground="#CC7A00")
        self.text.tag_configure("Token.Comment", foreground="#B80000")
        self.text.tag_configure("Token.Literal.String", foreground="#248F24")

    def _subscribe_to_repo_object_events(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        dependencies.pub_sub_broker.subscribe(
            self.id, self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_TEXT,
            lambda publisher, event, repo: self._get_text_update_from_repo(dependencies),
        )
        dependencies.pub_sub_broker.subscribe(
            self.id, self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_CHANGED_FONT,
            lambda publisher, event, repo: self._get_font_update_from_repo(dependencies),
        )
        dependencies.pub_sub_broker.subscribe(
            self.id, self.id,
            internal.objects.events.EVENT_TYPE_OBJECT_MOVED,
            lambda publisher, event, repo: self._get_move_update_from_repo(dependencies),
        )

    def _unsubscribe_from_repo_object_events(
        self, dependencies: internal.view.dependencies.Dependencies
    ):
        dependencies.pub_sub_broker.unsubscribe(VIEW_OBJECT_ID, self.id)

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
                internal.view.utils.get_lexers(),
                _LEXER_DESC,
                self._get_lexer,
                self._set_lexer,
            ),
        ]

    def _base_widget(
        self,
        dependencies: internal.view.dependencies.Dependencies,
        restrictions: List,
        description: str,
        getter: Callable,
        setter: Callable,
    ) -> List[tkinter.ttk.Widget]:
        string_var = tkinter.StringVar()
        label = tkinter.ttk.Label(
            dependencies.property_bar, text=description, justify='left', anchor='w'
        )
        combobox = tkinter.ttk.Combobox(
            dependencies.property_bar,
            textvariable=string_var,
            values=restrictions,
            state='readonly',
        )
        combobox.current(restrictions.index(getter(dependencies)))
        string_var.trace('w', lambda *_: setter(dependencies, string_var.get()))
        return label, combobox

    def _get_font_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectCode = dependencies.repo.get(self.id)
        font = obj.font
        tk_font = internal.view.utils.as_tkinter_object_font(font)
        self.text.configure(font=tk_font)

    def _get_text_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectText = dependencies.repo.get(self.id)
        self.text.delete('1.0', tkinter.END)
        self.text.insert(tkinter.END, obj.text)
        self.highlight()

    def _get_move_update_from_repo(self, dependencies: internal.view.dependencies.Dependencies):
        obj: internal.objects.interfaces.IBoardObjectCard = dependencies.repo.get(self.id)
        x = obj.position.x
        y = obj.position.y
        dependencies.canvas.coords(
            self.rectangle_id, x, y, x + _DEFAULT_WIDTH, y + _DEFAULT_HEIGHT
        )
        dependencies.canvas.coords(
            self.window_id, x + _DEFAULT_WIDTH / 2, y + _DEFAULT_HEIGHT / 2
        )

    def _get_lexer(self, dependencies: internal.view.dependencies.Dependencies):
        return self._lexer

    def _set_lexer(self, dependencies: internal.view.dependencies.Dependencies, value: str):
        dependencies.controller.edit_lexer(self.id, lexer=value)

    def destroy(self, dependencies: internal.view.dependencies.Dependencies):
        self._unsubscribe_from_repo_object_events(dependencies)
        ViewObject.destroy(self, dependencies)
