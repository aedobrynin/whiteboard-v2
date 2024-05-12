import typing
import logging

import internal.models


# TODO: stop using private controller fields (issue #29)
# TODO: somehow trigger linter error if class has no field
#       `_prop_name` (for example, text doesn't have property 'color')


class EditAction(internal.models.IAction):
    """Helper for simple assignment edit actions"""

    _controller: 'Controller'   # noqa: F821 (will be fixed in issue #29)
    _obj_id: internal.objects.interfaces.ObjectId
    _new_value: typing.Any
    _old_value: typing.Optional[typing.Any]
    _prop_name: str

    def __init__(
        self,
        controller: 'Controller',  # noqa: F821 (will be fixed in issue #29)
        obj_id: internal.objects.interfaces.ObjectId,
        property_name: str,
        new_value: typing.Any,
    ):
        self._controller = controller
        self._obj_id = obj_id
        self._prop_name = property_name
        self._new_value = new_value
        self._old_value = None

    def do(self):
        logging.debug(
            'trying to set %s=%s for obj with id=%s', self._prop_name, self._new_value, self._obj_id
        )
        obj = self._controller._repo.get(self._obj_id)
        if not obj:
            logging.warning(
                'EditAction::do() for property_name=%s: no obj with id=%s',
                self._prop_name,
                self._obj_id,
            )
            return
        self._old_value = getattr(obj, self._prop_name)
        setattr(obj, self._prop_name, self._new_value)
        self._controller._on_feature_finish()

    def undo(self):
        if self._old_value is None:   # TODO: what if old_value is actually None?
            logging.warning(
                'trying to undo action set %s=%s with old_value=None',
                self._prop_name,
                self._new_value,
            )
            return

        obj = self._controller._repo.get(self._obj_id)
        if not obj:
            logging.warning(
                'EditAction::do() for property_name=%s: no obj with id=%s',
                self._prop_name,
                self._obj_id,
            )
            return
        setattr(obj, self._prop_name, self._old_value)
        self._controller._on_feature_finish()
