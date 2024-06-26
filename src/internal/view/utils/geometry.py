from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class ScreenPosition:
    x: float
    y: float

    def __str__(self):
        return f'({self.x}, {self.y})'


class Rectangle:
    _top_left: ScreenPosition
    _bottom_right: ScreenPosition

    def __init__(self, a: ScreenPosition, b: ScreenPosition):
        self._top_left = ScreenPosition(min(a.x, b.x), min(a.y, b.y))
        self._bottom_right = ScreenPosition(max(a.x, b.x), max(a.y, b.y))

    def as_tkinter_rect(self) -> Tuple[int, int, int, int]:
        return self._top_left.x, self._top_left.y, self._bottom_right.x, self._bottom_right.y

    def get_width(self) -> int:
        return self._bottom_right.x - self._top_left.x

    def get_height(self) -> int:
        return self._bottom_right.y - self._top_left.y

    @property
    def top_left(self):
        return self._top_left

    @property
    def bottom_right(self):
        return self._bottom_right

    @staticmethod
    def from_tkinter_rect(rect: Tuple[int, int, int, int]) -> 'Rectangle':
        a = ScreenPosition(rect[0], rect[1])
        b = ScreenPosition(rect[2], rect[3])
        return Rectangle(a, b)

    def __str__(self):
        return f'Rect: a={self._top_left};b={self._bottom_right}'


def are_rects_intersecting(a: Rectangle, b: Rectangle) -> bool:
    return (
        a.top_left.x <= b.bottom_right.x
        and a.bottom_right.x >= b.top_left.x
        and a.top_left.y <= b.bottom_right.y
        and a.bottom_right.y >= b.top_left.y
    )


def get_min_containing_rect(a: Optional[Rectangle], b: Optional[Rectangle]) -> Optional[Rectangle]:
    if a is None:
        return b
    if b is None:
        return a

    res_a = ScreenPosition(min(a.top_left.x, b.top_left.x), min(a.top_left.y, b.top_left.y))
    res_b = ScreenPosition(
        max(a.bottom_right.x, b.bottom_right.x), max(a.bottom_right.y, b.bottom_right.y)
    )
    return Rectangle(res_a, res_b)
