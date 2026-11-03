"""画像とフォントの読み込み。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pygame

IMAGE_NAMES = (
    "player",
    "walker",
    "koopa",
    "shell",
    "solid",
    "question",
    "used",
    "flag",
)
FONT_SIZE = 14  # px


@dataclass(frozen=True)
class Assets:
    images: dict[str, pygame.Surface]
    font: pygame.font.Font


def load_assets(image_dir: Path) -> Assets:
    images = {
        name: pygame.image.load(str(image_dir / f"{name}.png")) for name in IMAGE_NAMES
    }
    return Assets(images=images, font=pygame.font.Font(None, FONT_SIZE))
