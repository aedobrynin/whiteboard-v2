from __future__ import annotations
import typing

import tkinter

import internal.view.dependencies
import internal.view.state_machine.interfaces


class State(internal.view.state_machine.interfaces.IState):
    _name: str
    _on_enter: typing.Callable[
        [internal.view.dependencies.Dependencies, typing.Dict, tkinter.Event], None
    ]
    _handle_event: typing.Callable[
        [internal.view.dependencies.Dependencies, typing.Dict, tkinter.Event], None
    ]
    _on_leave: typing.Callable[
        [internal.view.dependencies.Dependencies, typing.Dict, tkinter.Event], None
    ]

    def __init__(self, name: str):
        self._name = name
        self._transitions = []
        self._on_enter = lambda g, s, e: None
        self._handle_event = lambda g, s, e: None
        self._on_leave = lambda g, s, e: None

    @property
    def name(self) -> str:
        return self._name

    def set_on_enter(
        self,
        func: typing.Callable[
            [internal.view.dependencies.Dependencies, typing.Dict, tkinter.Event], None
        ],
    ):
        self._on_enter = func

    def on_enter(
        self,
        global_dependencies: internal.view.dependencies.Dependencies,
        state_ctx: typing.Dict,
        event: tkinter.Event,
    ):
        self._on_enter(global_dependencies, state_ctx, event)

    def set_event_handler(
        self,
        func: typing.Callable[
            [internal.view.dependencies.Dependencies, typing.Dict, tkinter.Event], None
        ],
    ):
        self._handle_event = func

    def handle_event(
        self,
        global_dependencies: internal.view.dependencies.Dependencies,
        state_ctx: typing.Dict,
        event: tkinter.Event,
    ):
        self._handle_event(global_dependencies, state_ctx, event)

    def set_on_leave(
        self,
        func: typing.Callable[
            [internal.view.dependencies.Dependencies, typing.Dict, tkinter.Event], None
        ],
    ):
        self._on_leave = func

    def on_leave(
        self,
        global_dependencies: internal.view.dependencies.Dependencies,
        state_ctx: typing.Dict,
        event: tkinter.Event,
    ):
        self._on_leave(global_dependencies, state_ctx, event)

    def __str__(self):
        return self.name
