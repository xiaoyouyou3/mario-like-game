"""ステージの文字列から StageData を作る。"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from src.game.constants import STAGE_H_TILES, STAGE_W_TILES, TILE_SIZE
from src.game.geometry import Aabb


class TileKind(Enum):
    EMPTY = 0
    SOLID = 1
    QUESTION = 2
    USED = 3


class StageFormatError(ValueError):
    """ステージ文字列の形式が不正なとき。"""


@dataclass(frozen=True)
class StageData:
    tiles: tuple[tuple[TileKind, ...], ...]
    start: tuple[int, int]
    walkers: tuple[tuple[int, int], ...]
    koopas: tuple[tuple[int, int], ...]
    flag: Aabb


_TILE_CHARS: dict[str, TileKind] = {
    ".": TileKind.EMPTY,
    "#": TileKind.SOLID,
    "?": TileKind.QUESTION,
}
_MARKER_CHARS = "PWKF"


def _parse_row(line: str, row: int) -> tuple[TileKind, ...]:
    if len(line) != STAGE_W_TILES:
        raise StageFormatError(
            f"row {row}: width {len(line)}, expected {STAGE_W_TILES}"
        )
    kinds: list[TileKind] = []
    for col, char in enumerate(line):
        if char in _TILE_CHARS:
            kinds.append(_TILE_CHARS[char])
        elif char in _MARKER_CHARS:
            kinds.append(TileKind.EMPTY)
        else:
            raise StageFormatError(f"unknown character {char!r} at ({col}, {row})")
    return tuple(kinds)


def _marker_cells(lines: list[str], marker: str) -> list[tuple[int, int]]:
    """読み順（行→列）でマーカーのマス (col, row) を返す。"""
    return [
        (col, row)
        for row, line in enumerate(lines)
        for col, char in enumerate(line)
        if char == marker
    ]


def _flag_box(cells: list[tuple[int, int]]) -> Aabb:
    cols = [c for c, _ in cells]
    rows = [r for _, r in cells]
    left, top = min(cols) * TILE_SIZE, min(rows) * TILE_SIZE
    return Aabb(
        left,
        top,
        (max(cols) + 1) * TILE_SIZE - left,
        (max(rows) + 1) * TILE_SIZE - top,
    )


def parse_stage(text: str) -> StageData:
    lines = text.splitlines()
    if len(lines) != STAGE_H_TILES:
        raise StageFormatError(f"height {len(lines)}, expected {STAGE_H_TILES}")
    tiles = tuple(_parse_row(line, row) for row, line in enumerate(lines))
    starts = _marker_cells(lines, "P")
    if len(starts) != 1:
        raise StageFormatError(f"start: need exactly one 'P', found {len(starts)}")
    flags = _marker_cells(lines, "F")
    if not flags:
        raise StageFormatError("flag: need at least one 'F'")
    return StageData(
        tiles=tiles,
        start=starts[0],
        walkers=tuple(_marker_cells(lines, "W")),
        koopas=tuple(_marker_cells(lines, "K")),
        flag=_flag_box(flags),
    )
