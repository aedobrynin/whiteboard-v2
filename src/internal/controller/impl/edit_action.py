import typing
import logging
import dataclasses

import internal.models

# TODO: tests
# TODO: stop using private controller fields (issue #29)
# TODO: somehow trigger linter error if class has no such property
#       (for example, text doesn't have property 'color')


@dataclasses.dataclass
class PropertyChange:
    property_name: str
    new_value: typing.Any


class EditAction(internal.models.IAction):
    """Helper for simple assignment edit actions"""

    _controller: 'Controller'   # noqa: F821 (will be fixed in issue #29)
    _obj_id: internal.objects.interfaces.ObjectId
    _changes: list[PropertyChange]
    _old_values: dict[str, typing.Any]

    def __init__(
        self,
        controller: 'Controller',  # noqa: F821 (will be fixed in issue #29)
        obj_id: internal.objects.interfaces.ObjectId,
        changes: list[PropertyChange],
    ):
        self._controller = controller
        self._obj_id = obj_id
        self._changes = changes
        self._old_values = {}

    def do(self):
        logging.debug('trying to make changes=%s for obj with id=%s', self._changes, self._obj_id)
        obj = self._controller._repo.get(self._obj_id)
        if not obj:
            logging.warning(
                'EditAction::do() for changes=%s: no obj with id=%s',
                self._changes,
                self._obj_id,
            )
            return

        for change in self._changes:
            self._old_values[change.property_name] = getattr(obj, change.property_name)
            setattr(obj, change.property_name, change.new_value)
        self._controller._on_feature_finish()

    def undo(self):
        obj = self._controller._repo.get(self._obj_id)
        if not obj:
            logging.warning(
                'EditAction::undo() for changes=%s: no obj with id=%s',
                self._changes,
                self._obj_id,
            )
            return

        for change in self._changes:
            if change.property_name not in self._old_values:
                logging.warning(
                    'EditAction::undo() no old_value for property_name=%s',
                    change.property_name,
                )
                continue
            setattr(obj, change.property_name, self._old_values[change.property_name])

        self._controller._on_feature_finish()
