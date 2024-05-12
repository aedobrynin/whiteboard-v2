import argparse
import logging
import pathlib

import internal.storages.impl
import internal.repositories.impl
import internal.controller.impl
import internal.pub_sub.impl
import internal.objects
import internal.view.view
import internal.undo_redo.impl

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

    logging.debug('initializing pubsub broker')
    broker = internal.pub_sub.impl.PubSubBroker()

    logging.debug('initializing storage')
    storage = internal.storages.impl.LocalYDocStorage(args['board-path'])
    serialized_objects = storage.get_serialized_objects()
    logging.debug('there are %d objects in storage', len(serialized_objects))
    objects = []
    for serialized_obj in serialized_objects.values():
        objects.append(internal.objects.build_from_serialized(serialized_obj, broker))
    logging.info('successfully parsed all objects from storage')

    logging.debug('initializing repo')
    repo = internal.repositories.impl.Repository(objects, broker)

    logging.debug('clearing created pub-sub events')
    broker.clear_events()

    undo_redo_manager_max_history_size = 100   # TODO: move to cfg
    logging.debug(
        'initializing undo-redo manager with max_history_size=%d',
        undo_redo_manager_max_history_size,
    )
    undo_redo_manager = internal.undo_redo.impl.UndoRedoManager(undo_redo_manager_max_history_size)

    logging.debug('initializing controller')
    controller = internal.controller.impl.Controller(repo, storage, broker, undo_redo_manager)

    logging.debug('initializing view')
    internal.view.view.main(controller=controller, repo=repo, pub_sub=broker)

    logging.info('shutting down...')
    storage.save()


if __name__ == '__main__':
    main()
