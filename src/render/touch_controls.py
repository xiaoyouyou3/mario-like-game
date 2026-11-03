"""仮想ボタンの配置と、タッチ座標から HeldButtons への変換。"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from src.game.geometry import Aabb
from src.game.input_state import HeldButtons


@dataclass(frozen=True)
class TouchLayout:
    left: Aabb
    right: Aabb
    jump: Aabb
    run: Aabb


def default_layout() -> TouchLayout:
    """内部解像度 256x240 の下端に、左右の移動ボタンを左、ダッシュとジャンプを右に置く。"""
    return TouchLayout(
        left=Aabb(8, 192, 40, 40),
        right=Aabb(56, 192, 40, 40),
        run=Aabb(160, 192, 40, 40),
        jump=Aabb(208, 192, 40, 40),
    )


def _is_pressed(box: Aabb, points: Sequence[tuple[float, float]]) -> bool:
    """左・上の辺は含み、右・下の辺は含まない。"""
    return any(
        box.left <= x < box.right and box.top <= y < box.bottom for x, y in points
    )


def points_to_held(
    points: Sequence[tuple[float, float]], layout: TouchLayout
) -> HeldButtons:
    """点が入っているボタンを押下とみなす。複数点で複数ボタン。"""
    return HeldButtons(
        left=_is_pressed(layout.left, points),
        right=_is_pressed(layout.right, points),
        jump=_is_pressed(layout.jump, points),
        run=_is_pressed(layout.run, points),
    )
