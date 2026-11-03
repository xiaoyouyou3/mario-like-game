"""カメラの追従。"""

from __future__ import annotations

from src.game.constants import CAMERA_FOLLOW_X, SCREEN_W


def next_camera_x(prev: float, player_center_x: float, level_width: float) -> float:
    """prev より小さくならず、0 以上かつ level_width - SCREEN_W 以下に収める。"""
    followed = max(prev, player_center_x - CAMERA_FOLLOW_X)
    return min(followed, level_width - SCREEN_W)
