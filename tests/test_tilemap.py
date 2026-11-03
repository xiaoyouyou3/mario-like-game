"""DES-005 tilemap のテスト。"""

from __future__ import annotations

import pytest

from src.game.stage_data import StageData, TileKind, parse_stage
from src.game.tilemap import TileMap
from tests.conftest import stage_text


def _data() -> StageData:
    return parse_stage(stage_text({(2, 1): "#", (3, 1): "?"}))


# TC-017
@pytest.mark.parametrize(("col", "expected"), [(1, False), (2, True), (3, True)])
def test_is_solid_is_true_for_solid_and_question_tiles_only(col: int, expected: bool) -> None:
    tilemap = TileMap(_data())

    result = tilemap.is_solid(col, 1)

    assert result is expected


# TC-017
def test_is_solid_is_true_for_a_used_tile() -> None:
    tilemap = TileMap(_data())
    assert tilemap.hit_question(3, 1)

    result = tilemap.is_solid(3, 1)

    assert result is True


# TC-018
@pytest.mark.parametrize(
    ("col", "row", "expected"),
    [(-1, 5, True), (200, 5, True), (0, -1, False), (0, 15, False)],
)
def test_is_solid_treats_left_and_right_edges_as_walls(col: int, row: int, expected: bool) -> None:
    tilemap = TileMap(_data())

    result = tilemap.is_solid(col, row)

    assert result is expected


# TC-019
def test_hit_question_turns_a_question_tile_into_used() -> None:
    tilemap = TileMap(_data())

    returned = tilemap.hit_question(3, 1)

    assert (returned, tilemap.tile_at(3, 1)) == (True, TileKind.USED)


# TC-020
def test_hit_question_changes_nothing_for_non_question_tiles() -> None:
    tilemap = TileMap(_data())
    assert tilemap.hit_question(3, 1)

    results = [tilemap.hit_question(c, 1) for c in (3, 2, 1)]

    kinds = [tilemap.tile_at(c, 1) for c in (3, 2, 1)]
    assert (results, kinds) == ([False, False, False], [TileKind.USED, TileKind.SOLID, TileKind.EMPTY])


# TC-021
def test_a_new_tilemap_from_the_same_data_starts_with_unhit_question_tiles() -> None:
    data = _data()
    first = TileMap(data)
    assert first.hit_question(3, 1)

    second = TileMap(data)

    assert (second.tile_at(3, 1), data.tiles[1][3]) == (TileKind.QUESTION, TileKind.QUESTION)
