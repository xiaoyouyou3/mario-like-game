"""矩形とタイル番号の計算。"""

from __future__ import annotations

import math
from dataclasses import dataclass

from src.game.constants import TILE_SIZE


@dataclass
class Aabb:
    x: float
    y: float
    w: float
    h: float

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def top(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        return self.y + self.h

    @property
    def center_x(self) -> float:
        return self.x + self.w / 2

    def overlaps(self, other: Aabb) -> bool:
        """辺が接するだけのときは偽。"""
        return (
            self.left < other.right
            and other.left < self.right
            and self.top < other.bottom
            and other.top < self.bottom
        )


def tile_span(lo: float, hi: float) -> range:
    """半開区間 [lo, hi) が重なるタイル番号の範囲。負の値でも floor で数える。"""
    return range(math.floor(lo / TILE_SIZE), math.ceil(hi / TILE_SIZE))
