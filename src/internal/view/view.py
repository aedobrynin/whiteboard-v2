<<<<<<< HEAD
import asyncio
import logging
=======
>>>>>>> main
import tkinter
import tkinter.font
import tkinter.ttk

<<<<<<< HEAD
import _tkinter

import internal.controller.interfaces
import internal.objects.interfaces
import internal.pub_sub.interfaces
import internal.repositories.events
import internal.repositories.interfaces
import internal.view.dependencies
import internal.view.modules.drag_board
import internal.view.modules.modules
import internal.view.modules.move_object
import internal.view.modules.submenu
import internal.view.modules.text
import internal.view.objects.impl.object_storage
import internal.view.state_machine.impl.state_machine
from internal.view.menu.impl.menu import Menu


async def root_update(
    view: tkinter.Tk
):
    while True:
        # Process all pending events
        while view.dooneevent(_tkinter.DONT_WAIT) > 0:
            pass
        try:
            view.winfo_exists()  # Will throw TclError if the main window is destroyed
        except tkinter.TclError:
            logging.debug('tkinter window closed')
            break
        await asyncio.sleep(0.01)


=======
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
import internal.view.modules.submenu
import internal.view.state_machine.impl.state_machine
import internal.view.objects.impl.object_storage
from internal.view.menu.impl.menu import Menu


>>>>>>> main
def _create_dependencies(
    root: tkinter.Tk,
    controller: internal.controller.interfaces.IController,
    repo: internal.repositories.interfaces.IRepository,
<<<<<<< HEAD
    pub_sub: internal.pub_sub.interfaces.IPubSubBroker
=======
    pub_sub: internal.pub_sub.interfaces.IPubSubBroker,
>>>>>>> main
) -> internal.view.dependencies.Dependencies:
    """
    Initializing dependencies
    """
    dependencies = internal.view.dependencies.Dependencies()
    canvas = tkinter.Canvas(root, width=700, height=500, bg='white')
    canvas.pack(side='left', fill='both', expand=False)
    menu = Menu(root)
    dependencies.root = root
    dependencies.canvas = canvas
    dependencies.controller = controller
    dependencies.repo = repo
    dependencies.pub_sub_broker = pub_sub
    dependencies.menu = menu
    dependencies.objects_storage = internal.view.objects.impl.object_storage.ViewObjectStorage(
        dependencies
    )
    dependencies.property_bar = tkinter.ttk.Frame(root)
    dependencies.property_bar.pack(fill='both', expand=True, padx=10, pady=10)
    state_machine = internal.view.state_machine.impl.state_machine.StateMachine(dependencies)
    dependencies.state_machine = state_machine
    return dependencies


<<<<<<< HEAD
def create_view(
    controller: internal.controller.interfaces.IController,
    repo: internal.repositories.interfaces.IRepository,
    pub_sub: internal.pub_sub.interfaces.IPubSubBroker,
    board_name: str = 'Whiteboard'
):
    root_window = tkinter.Tk(className=board_name)
=======
def main(
    controller: internal.controller.interfaces.IController,
    repo: internal.repositories.interfaces.IRepository,
    pub_sub: internal.pub_sub.interfaces.IPubSubBroker,
):
    root_window = tkinter.Tk(className='Whiteboard')
>>>>>>> main
    root_window.geometry('870x600')
    dependencies = _create_dependencies(root_window, controller, repo, pub_sub)
    dependencies.canvas.focus_set()
    internal.view.modules.modules.init_modules(dependencies)
    dependencies.objects_storage.create_view_objects(dependencies)
<<<<<<< HEAD
    return root_window
=======
    root_window.mainloop()
>>>>>>> main
