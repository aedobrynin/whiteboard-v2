import logging
import tkinter
import tkinter.ttk

import internal.controller.interfaces
import internal.repositories.interfaces
import internal.pub_sub.interfaces
import internal.view.menu.impl.menu
import internal.view.state_machine.impl.state_machine


class Dependencies:
    """
    There we collect all needed dependencies for view
    """
    root: tkinter.Tk
    canvas: tkinter.Canvas
    property_bar: tkinter.ttk.Frame
    menu: internal.view.menu.impl.menu.Menu
    logger: logging.Logger
    state_machine: internal.view.state_machine.impl.state_machine.StateMachine
    controller: internal.controller.interfaces.IController
    repo: internal.repositories.interfaces.IRepository
    pub_sub_broker: internal.pub_sub.interfaces.IPubSubBroker
