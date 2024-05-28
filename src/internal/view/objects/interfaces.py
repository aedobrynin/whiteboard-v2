from __future__ import annotations
import abc
from typing import Type, Optional

import internal.objects.interfaces
import internal.view.dependencies
import internal.view.utils


class IViewObject(abc.ABC):
    @property
    @abc.abstractmethod
    def id(self) -> internal.objects.interfaces.ObjectId:
        pass

    @abc.abstractmethod
    def destroy(self, dependencies: internal.view.dependencies.Dependencies) -> None:
        pass

    @abc.abstractmethod
    def set_focused(
        self, dependencies: internal.view.dependencies.Dependencies, is_focus: bool
    ) -> None:
        pass

    @abc.abstractmethod
    def get_focused(self, dependencies: internal.view.dependencies.Dependencies) -> bool:
        pass

    @abc.abstractmethod
    def move(
        self, dependencies: internal.view.dependencies.Dependencies, delta_x: int, delta_y: int
    ) -> None:
        pass

    @abc.abstractmethod
    def move_to(
        self, dependencies: internal.view.dependencies.Dependencies, x: int, y: int
    ) -> None:
        pass

    @abc.abstractmethod
    def get_border_rectangle(
        self, dependencies: internal.view.dependencies.Dependencies
    ) -> internal.view.utils.geometry.Rectangle:
        pass

    @abc.abstractmethod
    def draw_object_border(self, dependencies: internal.view.dependencies.Dependencies) -> None:
        pass

    @abc.abstractmethod
    def remove_object_border(self, dependencies: internal.view.dependencies.Dependencies) -> None:
        pass

    @abc.abstractmethod
    def aligning(self, dependencies: internal.view.dependencies.Dependencies) -> None:
        pass

    @abc.abstractmethod
    def scale(self, dependencies: internal.view.dependencies.Dependencies) -> None:
        pass

    @abc.abstractmethod
    def remove_aligning(self, dependencies: internal.view.dependencies.Dependencies) -> None:
        pass


class IViewObjectStorage(abc.ABC):
    @abc.abstractmethod
    def create_view_objects(self, dependencies: internal.view.dependencies.Dependencies) -> None:
        pass

    @abc.abstractmethod
    def register_object_type(self, type_name: str, type_class: Type[IViewObject]):
        pass

    @abc.abstractmethod
    def get_by_id(self, object_id: str) -> IViewObject:
        pass

    @abc.abstractmethod
    def get_opt_by_id(self, object_id: str) -> Optional[IViewObject]:
        pass

    @abc.abstractmethod
    def get_current(self, dependencies: internal.view.dependencies.Dependencies) -> IViewObject:
        pass

    @abc.abstractmethod
    def get_current_opt(
        self, dependencies: internal.view.dependencies.Dependencies
    ) -> Optional[IViewObject]:
        pass
