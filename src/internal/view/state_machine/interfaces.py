from __future__ import annotations
import abc
import typing

import tkinter

import internal.view.dependencies

ROOT_STATE_NAME = 'ROOT'
OBJECT_FOCUS_STATE_NAME = 'OBJECT-FOCUS'


class IState(abc.ABC):
    @abc.abstractmethod
    def __init__(self, name: str):  # noqa
        pass

    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def set_on_enter(
        self, func: typing.Callable[
            [internal.view.dependencies.Dependencies, typing.Dict, tkinter.Event], None]
    ):
        pass

    @abc.abstractmethod
    def on_enter(
        self,
        global_dependencies: internal.view.dependencies.Dependencies,
        state_ctx: typing.Dict,
        event: tkinter.Event
    ):
        pass

    @abc.abstractmethod
    def set_event_handler(
        self,
        func: typing.Callable[[
            internal.view.dependencies.Dependencies,
            typing.Dict,
            tkinter.Event
        ], None]
    ):
        pass

    @abc.abstractmethod
    def handle_event(
        self, global_dependencies: internal.view.dependencies.Dependencies, state_ctx: typing.Dict,
        event: tkinter.Event
    ):
        pass

    @abc.abstractmethod
    def set_on_leave(
        self, func: typing.Callable[
            [internal.view.dependencies.Dependencies, typing.Dict, tkinter.Event], None]
    ):
        pass

    @abc.abstractmethod
    def on_leave(
        self, global_dependencies: internal.view.dependencies.Dependencies, state_ctx: typing.Dict,
        event: tkinter.Event
    ):
        pass


class IStateMachine(abc.ABC):

    @abc.abstractmethod
    def add_state(self, state: IState):
        pass

    @abc.abstractmethod
    def add_transition(
        self, before: str, after: str,
        predicate: typing.Callable[[internal.view.dependencies.Dependencies, tkinter.Event], bool]
    ):
        pass

    @abc.abstractmethod
    def handle_event(self, event: tkinter.Event):
        pass

    @property
    @abc.abstractmethod
    def cur_state_name(self) -> str:
        pass
