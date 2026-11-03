"""キーボード入力と端末判定。"""

from __future__ import annotations

import sys
from collections.abc import Mapping

import pygame

from src.game.input_state import HeldButtons


def keys_to_held(pressed: Mapping[int, bool]) -> HeldButtons:
    """←→ で移動、Z でジャンプ、X でダッシュ。"""
    return HeldButtons(
        left=bool(pressed[pygame.K_LEFT]),
        right=bool(pressed[pygame.K_RIGHT]),
        jump=bool(pressed[pygame.K_z]),
        run=bool(pressed[pygame.K_x]),
    )


def detect_touch_device() -> bool:
    """ブラウザ実行時は navigator.maxTouchPoints > 0。それ以外は False。"""
    if sys.platform != "emscripten":
        return False
    import platform

    return bool(platform.window.navigator.maxTouchPoints > 0)  # type: ignore[attr-defined]
