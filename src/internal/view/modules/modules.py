import logging
from typing import List

import internal.view.dependencies

__MODULES = {}
__MODULE_DEPENDENCIES = {}


def register_module(module_name: str, dependencies: List[str] = []):  # noqa
    def __register(init_func):
        if module_name in __MODULES:
            raise AttributeError(f'module with name {module_name} was already registered')
        __MODULES[module_name] = init_func
        __MODULE_DEPENDENCIES[module_name] = dependencies
        return init_func

    return __register


def init_modules(dependencies: internal.view.dependencies.Dependencies):
    for module_name, init_func in __MODULES.items():
        for dependency_name in __MODULE_DEPENDENCIES[module_name]:
            if dependency_name not in __MODULES:
                logging.warning(
                    f'Skipped module \'{module_name}\' initialization: it depends on module '
                    f'\'{dependency_name}\' which was not registered'
                )
        init_func(dependencies)
