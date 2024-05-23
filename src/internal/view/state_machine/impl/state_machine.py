from __future__ import annotations

import logging
from typing import Callable
from typing import Dict
from typing import List
import tkinter

import internal.view.dependencies
import internal.view.state_machine.interfaces
from .state import State


class StateMachine(internal.view.state_machine.interfaces.IStateMachine):
    class _TransitionDescription:
        before: str
        after: str
        predicate: Callable[[internal.view.dependencies.Dependencies, tkinter.Event], bool]

    _states: Dict[str, State]  # name -> State
    _transitions: Dict[str, List[_TransitionDescription]]  # before -> after
    _cur_state: State
    _cur_state_context: Dict
    _global_dependencies: internal.view.dependencies.Dependencies

    def __init__(self, dependencies: internal.view.dependencies.Dependencies):
        self._global_dependencies = dependencies
        self._states = {}
        self._transitions = {}

        self._cur_state = self._make_root_state()
        self._cur_state_context = self._make_empty_context()

        self._start_listening()

    def _make_root_state(self):
        root_state = State(internal.view.state_machine.interfaces.ROOT_STATE_NAME)
        self.add_state(root_state)
        return root_state

    # noinspection PyMethodMayBeStatic
    def _make_empty_context(self):
        return {}

    def _start_listening(self):
        # click to left button of mouse
        self._global_dependencies.canvas.bind('<ButtonPress-1>', self.handle_event)
        # click to right button of mouse
        self._global_dependencies.canvas.bind('<ButtonPress-3>', self.handle_event)
        # motion by mouse
        self._global_dependencies.canvas.bind('<B1-Motion>', self.handle_event)
        # any key pressed on the keyboard
        self._global_dependencies.canvas.bind('<Key>', self.handle_event)
        # any key is released on the keyboard
        self._global_dependencies.canvas.bind('<KeyRelease>', self.handle_event)
        # combination of shift+left-button-mouse
        self._global_dependencies.canvas.bind('<Shift-ButtonPress-1>', self.handle_event)
        # on release of pressed left button mouse
        self._global_dependencies.canvas.bind('<ButtonRelease-1>', self.handle_event)
        # on release of right button mouse
        self._global_dependencies.canvas.bind('<ButtonRelease-3>', self.handle_event)
        # combination of control+left-button-mouse
        self._global_dependencies.canvas.bind('<Control-ButtonPress-1>', self.handle_event)
        # menu bind
        self._global_dependencies.menu.bind(self.handle_event)

    def add_state(self, state: State):
        self._states[state.name] = state

    def add_transition(
        self,
        before: str,
        after: str,
        predicate: Callable[[internal.view.dependencies.Dependencies, tkinter.Event], bool],
    ):
        tr_description = StateMachine._TransitionDescription()
        tr_description.before = before
        tr_description.after = after
        tr_description.predicate = predicate
        if before not in self._transitions:
            self._transitions[before] = []
        self._transitions[before].append(tr_description)

    def handle_event(self, event: tkinter.Event):
        logging.debug('StateMachine: trying to match event to transition predicates')
        for tr_description in self._transitions.get(self._cur_state.name, []):
            if tr_description.predicate(self._global_dependencies, event):
                logging.debug('trying to change state after predicate')
                after_state = self._states.get(tr_description.after)
                if not after_state:
                    logging.error('after-state in state-machine is empty')
                    return
                state_changed_from = self._cur_state.name
                logging.debug('leaving from before-state (%s) in state-machine', state_changed_from)
                self._cur_state.on_leave(self._global_dependencies, self._cur_state_context, event)
                self._cur_state_context = self._make_empty_context()
                self._cur_state = after_state
                logging.debug('entering to after-state (%s) in state-machine', after_state)
                self._cur_state.on_enter(self._global_dependencies, self._cur_state_context, event)
                return

        logging.debug(
            "StateMachine: couldn't match event to any transition predicate, pass it to current state"
        )
        self._cur_state.handle_event(self._global_dependencies, self._cur_state_context, event)
