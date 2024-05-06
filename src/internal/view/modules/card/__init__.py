from __future__ import annotations

import internal.view.dependencies
from .states import create_card, change_card
from .view import create_card_object as create_card_object


def create_states(dependencies: internal.view.dependencies):
    dependencies.state_machine.add_state(create_card.create_state(dependencies.state_machine))
    dependencies.state_machine.add_state(change_card.create_state(dependencies.state_machine))


def register_module_menu(dependencies: internal.view.dependencies):
    dependencies.menu.add_command_to_menu(create_card.CARD_MENU_ENTRY_NAME)


@internal.view.modules.modules.register_module('card')
def init_module(dependencies: internal.view.dependencies):
    create_states(dependencies)
    register_module_menu(dependencies)