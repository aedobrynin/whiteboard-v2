import tkinter
from .card_view import CanvasTextObject
from .context import Context
from ..controller.interfaces import IController
from ..models import Position
from ..objects import BoardObjectType
from ..objects.interfaces import IBoardObject
from ..repositories.interfaces import IRepository, REPOSITORY_PUB_SUB_ID
from ..repositories.events import EVENT_TYPE_OBJECT_ADDED, EVENT_TYPE_OBJECT_DELETED, EventObjectAdded
from ..pub_sub.interfaces import IPubSubBroker
from .drag_view import bind_on_events as drag_bind_on_events


class TkinterTk(tkinter.Tk):
    def __init__(self, controller: IController, repo: IRepository, broker: IPubSubBroker):
        super().__init__()
        self.geometry('870x600')

        canvas = tkinter.Canvas(self, width=700, height=500, bg='white')
        canvas.pack(side='left', fill='both', expand=False)

        self.broker = broker
        self._subscribe()

        self.context = Context()
        self.context.controller = controller
        self.context.repo = repo
        self.context.canvas = canvas

        drag_bind_on_events(self.context)
        canvas.bind('<Shift-ButtonPress-1>', self._create_text_canvas)

    def _subscribe(self):
        self.broker.subscribe(
            'view',
            REPOSITORY_PUB_SUB_ID,
            EVENT_TYPE_OBJECT_ADDED,
            self._create_obj
        )

        self.broker.subscribe(
            'view',
            REPOSITORY_PUB_SUB_ID,
            EVENT_TYPE_OBJECT_DELETED,
            self._delete_obj
        )

    def _create_text_canvas(self, event: tkinter.Event):
        self.context.controller.create_object(
            BoardObjectType.CARD,
            Position(x=event.x, y=event.y, z=1)
        )

    def _create_obj(self, _: str, event: EventObjectAdded, repo: IRepository):
        obj: IBoardObject = repo.get(event.object_id)
        if obj.type == BoardObjectType.CARD:
            CanvasTextObject(self.context, event.object_id)
        else:
            pass

    def _delete_obj(self, _: str, event: EventObjectAdded, repo: IRepository):
        pass
