from __future__ import annotations
import abc

import internal.models
import internal.objects


class IController(abc.ABC):
    @abc.abstractmethod
    def create_object(
        self, type: internal.objects.BoardObjectType, position: internal.models.Position
    ):
        pass
