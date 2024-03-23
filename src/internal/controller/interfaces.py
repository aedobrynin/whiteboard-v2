from __future__ import annotations
import abc

import internal.models
import internal.objects


class IController(abc.ABC):
    # TODO: feature abstaction
    @abc.abstractmethod
    def create_object(
        self, type: internal.objects.BoardObjectType, position: internal.models.Position
    ):
        pass
