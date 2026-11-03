"""タイルの固体判定と ? ブロックの状態変更。"""

from __future__ import annotations

from src.game.stage_data import StageData, TileKind


class TileMap:
    def __init__(self, data: StageData) -> None:
        self._tiles: list[list[TileKind]] = [list(row) for row in data.tiles]
        self._width = len(self._tiles[0])
        self._height = len(self._tiles)

    def is_solid(self, col: int, row: int) -> bool:
        if col < 0 or col >= self._width:
            return True
        if row < 0 or row >= self._height:
            return False
        return self._tiles[row][col] is not TileKind.EMPTY

    def tile_at(self, col: int, row: int) -> TileKind:
        return self._tiles[row][col]

    def hit_question(self, col: int, row: int) -> bool:
        if self._tiles[row][col] is not TileKind.QUESTION:
            return False
        self._tiles[row][col] = TileKind.USED
        return True
