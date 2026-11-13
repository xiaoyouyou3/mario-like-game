"""仮想ボタンの配置と、タッチ座標から HeldButtons への変換。"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from src.game.constants import PLAY_H, SCREEN_W, TOUCH_BUTTON_SIZE
from src.game.geometry import Aabb
from src.game.input_state import HeldButtons


@dataclass(frozen=True)
class TouchLayout:
    left: Aabb
    right: Aabb
    jump: Aabb
    run: Aabb


PANEL_MARGIN = 8  # px 操作パネルの上端とボタンの間、ボタン同士の間
SIDE_MARGIN = 16  # px 画面の左右端とボタンの間


def default_layout() -> TouchLayout:
    """操作パネル（y >= PLAY_H）の中に、左右の移動ボタンを左、ダッシュとジャンプを右に置く。"""
    size = TOUCH_BUTTON_SIZE
    top = PLAY_H + PANEL_MARGIN
    right_x = SIDE_MARGIN + size + PANEL_MARGIN
    jump_x = SCREEN_W - SIDE_MARGIN - size
    run_x = jump_x - PANEL_MARGIN - size
    return TouchLayout(
        left=Aabb(SIDE_MARGIN, top, size, size),
        right=Aabb(right_x, top, size, size),
        run=Aabb(run_x, top, size, size),
        jump=Aabb(jump_x, top, size, size),
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
