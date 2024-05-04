import logging
import typing

import internal.objects.interfaces
import internal.view.dependencies


def get_current(
    global_dependencies: internal.view.dependencies.Dependencies
) -> internal.objects.interfaces.IBoardObject:
    tags = global_dependencies.canvas.gettags('current')
    if not tags:
        logging.error('No tags for current object')
        raise KeyError('No tags for current object')
    obj = global_dependencies.repo.get(tags[0])
    if obj:
        return obj
    global_dependencies.logger.error('Empty object list from repo')
    raise KeyError('No tags for current object')


def get_current_opt(
    global_dependencies: internal.view.dependencies.Dependencies
) -> typing.Optional[internal.objects.interfaces.IBoardObject]:
    tags = global_dependencies.canvas.gettags('current')
    if not tags:
        logging.debug('No tags for current object')
        return None
    return global_dependencies.repo.get(tags[0])


def get_current_opt_type(
    global_dependencies: internal.view.dependencies.Dependencies
) -> str:
    tags = global_dependencies.canvas.gettags('current')
    if not tags or len(tags) < 2:
        logging.debug('No other tags found')
        return ''
    return tags[1]

def get_current_tags(
    global_dependencies: internal.view.dependencies.Dependencies
) -> internal.objects.interfaces.IBoardObject:
    tags = global_dependencies.canvas.gettags('current')
    if not tags:
        logging.error('No tags for current object')
        raise KeyError('No tags for current object')
    return tags