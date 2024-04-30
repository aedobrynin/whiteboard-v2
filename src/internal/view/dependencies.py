import tkinter

from ..controller import interfaces as controller_interfaces
from ..repositories import interfaces as repo_interfaces


class Depen:
    controller: controller_interfaces.IController
    repo: repo_interfaces.IRepository
    canvas: tkinter.Canvas

import logging
import tkinter
from tkinter import ttk

from menu import Menu
from objects_storage import ObjectsStorage
from state_machine import StateMachine
from pub_sub import Broker


class Context:
    root: tkinter.Tk
    events_history: events.events_history.EventsHistory
    event_handlers: events.event_handlers.EventHandlers
    objects_storage: ObjectsStorage
    logger: logging.Logger
    canvas: tkinter.Canvas
    state_machine: StateMachine
    property_bar: ttk.Frame
    menu: Menu
    pub_sub_broker: Broker