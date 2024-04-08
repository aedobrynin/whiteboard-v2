import tkinter

from ..controller import interfaces as controller_interfaces
from ..repositories import interfaces as repo_interfaces


class Context:
    controller: controller_interfaces.IController
    repo: repo_interfaces.IRepository
    canvas: tkinter.Canvas
