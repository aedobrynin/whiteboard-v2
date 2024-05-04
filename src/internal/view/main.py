import logging
import tkinter
import tkinter.font
import tkinter.ttk

import internal.controller.interfaces
import internal.repositories.interfaces
import internal.repositories.events
import internal.pub_sub.interfaces
import internal.objects.interfaces
import internal.view.dependencies
import internal.view.modules.modules
import internal.view.modules.drag_board
import internal.view.modules.move_object
import internal.view.modules.text
import internal.view.modules.card
import internal.view.modules.pen

import internal.view.modules.submenu
import internal.view.state_machine.impl.state_machine
from internal.view.menu.impl.menu import Menu

dependencies = internal.view.dependencies.Dependencies()


def _fill_dependencies(
    root: tkinter.Tk,
    controller: internal.controller.interfaces.IController,
    repo: internal.repositories.interfaces.IRepository,
    pub_sub: internal.pub_sub.interfaces.IPubSubBroker
) -> internal.view.dependencies.Dependencies:
    """
    Initializing dependencies of canvas
    """
    canvas = tkinter.Canvas(root, width=700, height=500, bg='white')
    canvas.pack(side='left', fill='both', expand=False)
    menu = Menu(root)

    dependencies.root = root
    dependencies.canvas = canvas
    dependencies.controller = controller
    dependencies.repo = repo
    dependencies.pub_sub_broker = pub_sub
    dependencies.menu = menu
    dependencies.property_bar = tkinter.ttk.Frame(root)
    dependencies.property_bar.pack(fill='both', expand=True, padx=10, pady=10)
    state_machine = internal.view.state_machine.impl.state_machine.StateMachine(dependencies)
    dependencies.state_machine = state_machine


def _init_repo_objects(
    repo: internal.repositories.interfaces.IRepository
):
    """
    Creating all saved objects on canvas
    """
    for obj in repo.get_all():
        _create_obj(obj)


def _subscribe(
    broker: internal.pub_sub.interfaces.IPubSubBroker
):
    """
    Subscribing view to events
    """
    broker.subscribe(
        'view',
        internal.repositories.interfaces.REPOSITORY_PUB_SUB_ID,
        internal.repositories.events.EVENT_TYPE_OBJECT_ADDED,
        _create_obj_event
    )
    broker.subscribe(
        'view',
        internal.repositories.interfaces.REPOSITORY_PUB_SUB_ID,
        internal.repositories.events.EVENT_TYPE_OBJECT_DELETED,
        _delete_obj_event
    )


def _create_obj_event(
    publisher: internal.pub_sub.interfaces.PublisherId,
    event: internal.repositories.events.EVENT_TYPE_OBJECT_ADDED,
    repo: internal.repositories.interfaces.IRepository
):
    """
    Callback of creating object from repo
    """
    obj: internal.objects.interfaces.IBoardObject = repo.get(event.object_id)
    _create_obj(obj)


def _delete_obj_event(
    publisher: internal.pub_sub.interfaces.PublisherId,
    event: internal.repositories.events.EVENT_TYPE_OBJECT_DELETED,
    repo: internal.repositories.interfaces.IRepository
):
    """
       Callback of deleting object from repo
    """
    logging.debug('deleting the object=%s from canvas', event.object_id)
    dependencies.canvas.delete(event.object_id)


def _create_obj(obj: internal.objects.interfaces.IBoardObject):
    """
    each module initiate its own canvas object
    """
    if obj.type == internal.objects.BoardObjectType.TEXT:
        internal.view.modules.text.create_text_object(dependencies, obj)
    if obj.type == internal.objects.BoardObjectType.CARD:
        internal.view.modules.card.create_card_object(dependencies, obj)
    if obj.type == internal.objects.BoardObjectType.PEN:
        internal.view.modules.pen.create_pen_object(dependencies, obj)


def main(
    controller: internal.controller.interfaces.IController,
    repo: internal.repositories.interfaces.IRepository,
    pub_sub: internal.pub_sub.interfaces.IPubSubBroker
):
    root_window = tkinter.Tk(className='Whiteboard')
    root_window.geometry('870x600')
    _subscribe(pub_sub)
    _fill_dependencies(root_window, controller, repo, pub_sub)
    _init_repo_objects(repo)
    dependencies.canvas.focus_set()
    internal.view.modules.modules.init_modules(dependencies)
    root_window.mainloop()
