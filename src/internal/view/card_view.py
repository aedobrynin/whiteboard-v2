import tkinter

from . import context
from ..objects.interfaces import IBoardObjectCard, ObjectId
from ..controller.interfaces import ICardController
from ..controller.impl import CardController


class CanvasTextObject:
    def __init__(
        self,
        ctx: context.Context,
        obj_id: ObjectId
    ):

        self.ctx = ctx
        self.obj_id = obj_id
        self._text_id = self._create_canvas_text(obj_id)
        self.ctx.canvas.tag_bind(self._text_id, '<Double-ButtonRelease-1>', self._edit_text_start)
        self.edit_func_key: str = None
        self.edit_func_leave_key: str = None
        self.controller: ICardController = self.ctx.controller

    def _create_canvas_text(self, obj_id: ObjectId) -> int:
        card_obj: IBoardObjectCard = self.ctx.repo.get(object_id=obj_id)
        return self.ctx.canvas.create_text(
            card_obj.position.x,
            card_obj.position.y,
            text=card_obj.text,
            tags=[obj_id, 'text'],
            font=('Arial', 14)
        )

    def _edit_text_start(self, _: tkinter.Event):
        self.ctx.canvas.focus_set()
        bbox = self.ctx.canvas.bbox(self._text_id)
        self.ctx.canvas.icursor(self._text_id, f'@{bbox[2]},{bbox[3]}')
        self.ctx.canvas.focus(self._text_id)
        # we save func keys, to delete after
        self.edit_func_key = self.ctx.canvas.tag_bind(self._text_id, '<Key>', self._edit_text, add='+')
        self.edit_func_leave_key = self.ctx.canvas.bind('<ButtonPress-1>', self._edit_text_end, add='+')

    def _edit_text(self, event: tkinter.Event):
        if event.keysym == 'Right':
            new_index = self.ctx.canvas.index(self._text_id, 'insert') + 1
            self.ctx.canvas.icursor(self._text_id, new_index)
            self.ctx.canvas.select_clear()
            return

        if event.keysym == 'Left':
            new_index = self.ctx.canvas.index(self._text_id, 'insert') - 1
            self.ctx.canvas.icursor(self._text_id, new_index)
            self.ctx.canvas.select_clear()
            return

        if event.keysym == 'BackSpace':
            insert = self.ctx.canvas.index(self._text_id, 'insert')
            if insert > 0:
                self.ctx.canvas.dchars(self._text_id, insert - 1, insert - 1)
            return

        if event.char == '':
            return
        self.ctx.canvas.index(self._text_id, 'insert')
        self.ctx.canvas.insert(self._text_id, 'insert', event.char)

    def _edit_text_end(self, _: tkinter.Event):
        # update obj
        self.controller.edit_text(self.obj_id, self.ctx.canvas.itemcget(self._text_id, 'text'))
        # reset focus
        self.ctx.canvas.focus('')
        # delete bindings
        self.ctx.canvas.tag_unbind(self._text_id, '<Key>', self.edit_func_key)
        self.ctx.canvas.unbind('<ButtonPress-1>', self.edit_func_leave_key)
        # null func binding keys
        self.edit_func_key = None
        self.edit_func_leave_key = None
