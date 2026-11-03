"""ゲームで使うドット絵を生成する（外部素材は使わない）。

使い方: .venv/bin/python scripts/make_assets.py
出力: assets/images/*.png
"""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

OUT = Path(__file__).resolve().parent.parent / "assets" / "images"

Color = tuple[int, int, int]
CLEAR = (0, 0, 0, 0)
BROWN: Color = (152, 84, 36)
DARK: Color = (88, 48, 20)
SAND: Color = (240, 200, 140)
RED: Color = (216, 40, 32)
BLUE: Color = (40, 72, 200)
WHITE: Color = (255, 255, 255)
BLACK: Color = (0, 0, 0)
GREEN: Color = (48, 160, 56)
DGREEN: Color = (24, 96, 40)
GOLD: Color = (252, 188, 56)
GRAY: Color = (136, 136, 136)


def _surface(w: int, h: int) -> pygame.Surface:
    return pygame.Surface((w, h), pygame.SRCALPHA)


def _rect(s: pygame.Surface, color: Color, x: int, y: int, w: int, h: int) -> None:
    pygame.draw.rect(s, color, (x, y, w, h))


def player() -> pygame.Surface:
    s = _surface(12, 16)
    _rect(s, RED, 2, 0, 8, 3)
    _rect(s, SAND, 2, 3, 8, 4)
    _rect(s, BLACK, 7, 4, 1, 2)
    _rect(s, RED, 1, 7, 10, 4)
    _rect(s, BLUE, 2, 9, 8, 4)
    _rect(s, BROWN, 1, 13, 4, 3)
    _rect(s, BROWN, 7, 13, 4, 3)
    return s


def walker() -> pygame.Surface:
    s = _surface(16, 16)
    _rect(s, BROWN, 2, 1, 12, 8)
    _rect(s, BROWN, 0, 6, 16, 4)
    _rect(s, SAND, 3, 10, 10, 3)
    _rect(s, DARK, 1, 13, 5, 3)
    _rect(s, DARK, 10, 13, 5, 3)
    _rect(s, WHITE, 3, 4, 3, 3)
    _rect(s, WHITE, 10, 4, 3, 3)
    _rect(s, BLACK, 4, 5, 1, 2)
    _rect(s, BLACK, 11, 5, 1, 2)
    return s


def koopa() -> pygame.Surface:
    s = _surface(16, 16)
    _rect(s, GREEN, 3, 5, 10, 8)
    _rect(s, DGREEN, 5, 7, 6, 4)
    _rect(s, SAND, 1, 0, 6, 6)
    _rect(s, BLACK, 2, 2, 1, 2)
    _rect(s, SAND, 4, 13, 8, 3)
    return s


def shell() -> pygame.Surface:
    s = _surface(16, 16)
    _rect(s, GREEN, 2, 4, 12, 9)
    _rect(s, DGREEN, 4, 6, 8, 5)
    _rect(s, SAND, 3, 13, 10, 2)
    return s


def solid() -> pygame.Surface:
    s = _surface(16, 16)
    s.fill(BROWN)
    pygame.draw.rect(s, DARK, (0, 0, 16, 16), 1)
    _rect(s, DARK, 0, 8, 16, 1)
    _rect(s, DARK, 8, 0, 1, 8)
    _rect(s, DARK, 4, 8, 1, 8)
    return s


def question() -> pygame.Surface:
    s = _surface(16, 16)
    s.fill(GOLD)
    pygame.draw.rect(s, DARK, (0, 0, 16, 16), 1)
    for x, y, w, h in [(5, 3, 6, 2), (9, 5, 2, 3), (7, 8, 3, 2), (7, 11, 2, 2)]:
        _rect(s, DARK, x, y, w, h)
    return s


def used() -> pygame.Surface:
    s = _surface(16, 16)
    s.fill(GRAY)
    pygame.draw.rect(s, DARK, (0, 0, 16, 16), 1)
    return s


def flag() -> pygame.Surface:
    s = _surface(16, 16)
    _rect(s, GRAY, 7, 0, 2, 16)
    _rect(s, GREEN, 9, 1, 7, 5)
    return s


SPRITES = {
    "player": player,
    "walker": walker,
    "koopa": koopa,
    "shell": shell,
    "solid": solid,
    "question": question,
    "used": used,
    "flag": flag,
}


def main() -> None:
    pygame.init()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, make in SPRITES.items():
        pygame.image.save(make(), str(OUT / f"{name}.png"))
    print(f"wrote {len(SPRITES)} sprites to {OUT}")


if __name__ == "__main__":
    main()
