"""DES-004 stage_data のテスト。"""

from __future__ import annotations

import pytest

from src.game.geometry import Aabb
from src.game.stage_data import StageFormatError, TileKind, parse_stage
from tests.conftest import stage_text


# TC-007
def test_parse_stage_reads_each_character_as_its_tile_kind() -> None:
    text = stage_text({(3, 14): "#", (5, 10): "?", (6, 14): ".", (9, 10): "F"})

    data = parse_stage(text)

    kinds = (
        data.tiles[14][3],
        data.tiles[10][5],
        data.tiles[14][6],
        data.tiles[13][2],
        data.tiles[10][9],
    )
    assert kinds == (TileKind.SOLID, TileKind.QUESTION, TileKind.EMPTY, TileKind.EMPTY, TileKind.EMPTY)


# TC-008
def test_parse_stage_reads_the_player_start_tile() -> None:
    text = stage_text({(2, 13): "P"})

    data = parse_stage(text)

    assert data.start == (2, 13)


# TC-009
def test_parse_stage_lists_walkers_and_koopas_in_reading_order() -> None:
    text = stage_text({(10, 13): "W", (20, 13): "W", (30, 13): "K"})

    data = parse_stage(text)

    assert (data.walkers, data.koopas) == (((10, 13), (20, 13)), ((30, 13),))


# TC-010
def test_parse_stage_bounds_all_flag_cells_with_one_box() -> None:
    text = stage_text({(198, 10): "F", (198, 11): "F", (198, 12): "F"})

    data = parse_stage(text)

    assert data.flag == Aabb(3168, 160, 16, 48)


# TC-011
def test_parse_stage_produces_a_grid_of_15_rows_and_200_columns() -> None:
    text = stage_text()

    data = parse_stage(text)

    assert (len(data.tiles), len(data.tiles[0])) == (15, 200)


# TC-012
def test_parse_stage_rejects_a_row_with_the_wrong_width() -> None:
    lines = stage_text().split("\n")
    lines[2] = lines[2][:-1]

    with pytest.raises(StageFormatError, match="width"):
        parse_stage("\n".join(lines))


# TC-013
@pytest.mark.parametrize("row_count", [14, 16])
def test_parse_stage_rejects_a_wrong_number_of_rows(row_count: int) -> None:
    lines = stage_text().split("\n")
    lines = lines[:row_count] if row_count < 15 else [*lines, "." * 200]

    with pytest.raises(StageFormatError, match="height"):
        parse_stage("\n".join(lines))


# TC-014
def test_parse_stage_rejects_an_unknown_character() -> None:
    text = stage_text({(4, 4): "X"})

    with pytest.raises(StageFormatError, match="unknown character"):
        parse_stage(text)


# TC-015
@pytest.mark.parametrize(
    ("cells", "start"),
    [({}, None), ({(2, 13): "P", (3, 13): "P"}, (2, 13))],
)
def test_parse_stage_requires_exactly_one_start(
    cells: dict[tuple[int, int], str], start: tuple[int, int] | None
) -> None:
    text = stage_text(cells, start=start)

    with pytest.raises(StageFormatError, match="start"):
        parse_stage(text)


# TC-016
def test_parse_stage_requires_at_least_one_flag_cell() -> None:
    text = stage_text(flag=None)

    with pytest.raises(StageFormatError, match="flag"):
        parse_stage(text)
