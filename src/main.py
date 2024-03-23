import argparse
import logging
import pathlib

import internal

_logging_choice_to_loglevel = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'board-path',
        type=pathlib.Path,
        help='path to board',
        nargs='?',
        default='storage.boardobj',
    )
    parser.add_argument(
        'logging-level',
        type=str,
        help='logging level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        nargs='?',
        default='DEBUG',
    )
    args = vars(parser.parse_args())

    logging.basicConfig(
        level=_logging_choice_to_loglevel[args['logging-level']],
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    logging.debug('initializing storage')
    storage = internal.storages.impl.LocalYDocStorage(args['board-path'])

    serialized_objects = storage.get_serialized_objects()
    logging.debug('there are %d objects in storage', len(serialized_objects))
    objects = []
    for serialized_obj in serialized_objects.values():
        objects.append(internal.objects.build_from_serialized(serialized_obj))
    logging.info('successfully parsed all objects from storage')

    logging.debug('initializing repo')
    repo = internal.repositories.impl.Repository(objects)

    logging.debug('initializing controller')
    controller = internal.controller.impl.Controller(repo, storage)   # noqa

    input('press enter to stop')

    logging.info('shutting down...')
    storage.save()


if __name__ == '__main__':
    main()
