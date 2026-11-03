"""DES-011 level のテスト。"""

from __future__ import annotations

import pytest

from src.game.input_state import InputState
from src.game.level import Level, LevelEvents, LevelStatus
from src.game.stage_data import TileKind, parse_stage
from tests.conftest import stage_text

DT = 1 / 60
NONE = InputState(left=False, right=False, run=False, jump_pressed=False)
RIGHT = InputState(left=False, right=True, run=False, jump_pressed=False)
JUMP = InputState(left=False, right=False, run=False, jump_pressed=True)

PLAYING = LevelStatus.PLAYING
DIED = LevelStatus.PLAYER_DIED
CLEARED = LevelStatus.CLEARED


def _level(cells: dict[tuple[int, int], str] | None = None, *, ground: bool = True) -> Level:
    return Level(parse_stage(stage_text(cells, ground=ground)))


def _grounded(cells: dict[tuple[int, int], str] | None = None) -> Level:
    """地面ありの Level を、入力なしで 1 ステップ進めて接地させる。"""
    level = _level(cells)
    level.step(NONE, DT)
    return level


def _steps(level: Level, inp: InputState, times: int) -> list[LevelEvents]:
    return [level.step(inp, DT) for _ in range(times)]


def _clearable_level() -> Level:
    flag = {(8, row): "F" for row in range(10, 14)}
    return _level({(7, 13): "P", **flag})


# TC-081
def test_level_places_the_player_and_enemies_from_the_stage() -> None:
    level = _level({(2, 13): "P", (10, 13): "W"})

    player_box = level.player.body.box
    enemy_boxes = [enemy.body.box for enemy in level.enemies]
    actual = (
        (player_box.x, player_box.y, player_box.w, player_box.h),
        [(box.x, box.y, box.w, box.h) for box in enemy_boxes],
        level.camera_x,
        level.status,
    )
    assert actual == ((34, 208, 12, 16), [(160, 208, 16, 16)], 0, PLAYING)


# TC-082
def test_level_does_not_advance_after_the_player_died() -> None:
    level = _level({(2, 13): "P", (10, 13): "W"})
    level.camera_x = 100
    level.player.body.box.x = 87.9
    level.step(NONE, DT)
    before = (level.player.body.box.x, level.player.body.box.y)

    events = level.step(RIGHT, DT)

    after = (level.player.body.box.x, level.player.body.box.y)
    assert (events.status, events.coins_gained, after) == (DIED, 0, before)


# TC-083
def test_level_removes_an_enemy_that_falls_below_the_stage() -> None:
    level = _level({(2, 13): "P", (10, 14): "W"}, ground=False)

    enemy_counts = []
    for _ in range(11):
        events = level.step(NONE, DT)
        enemy_counts.append(len(level.enemies))

    state = (enemy_counts, events.status, level.player.body.box.y)
    assert state == ([1] * 10 + [0], PLAYING, pytest.approx(224.5))


# TC-084
def test_level_awards_a_coin_when_the_player_hits_a_question_block() -> None:
    level = _grounded({(2, 13): "P", (2, 12): "?"})

    events = level.step(JUMP, DT)

    assert (events.coins_gained, level.tilemap.tile_at(2, 12)) == (1, TileKind.USED)


# TC-085
def test_level_gives_no_second_coin_from_a_used_block() -> None:
    level = _grounded({(2, 13): "P", (2, 12): "?"})
    level.step(JUMP, DT)
    level.step(NONE, DT)

    events = level.step(JUMP, DT)

    assert (events.coins_gained, level.tilemap.tile_at(2, 12)) == (0, TileKind.USED)


# TC-086
def test_level_gives_no_coin_from_a_solid_block() -> None:
    level = _grounded({(2, 13): "P", (2, 12): "#"})

    events = level.step(JUMP, DT)

    assert (events.coins_gained, level.tilemap.tile_at(2, 12)) == (0, TileKind.SOLID)


# TC-087
def test_level_kills_the_player_who_falls_below_the_stage() -> None:
    level = _level({(2, 13): "P"}, ground=False)

    events = _steps(level, NONE, 15)
    y_after_15 = level.player.body.box.y
    events.append(level.step(NONE, DT))

    statuses = [event.status for event in events]
    assert (statuses, y_after_15, level.player.body.box.y) == (
        [PLAYING] * 15 + [DIED],
        pytest.approx(238),
        pytest.approx(242),
    )


# TC-088
def test_level_is_cleared_when_the_player_overlaps_the_flag() -> None:
    level = _clearable_level()

    events = _steps(level, RIGHT, 5)

    assert [event.status for event in events] == [PLAYING] * 4 + [CLEARED]


# TC-089
def test_level_kills_the_player_who_walks_into_an_enemy() -> None:
    level = _level({(2, 13): "P", (3, 13): "W"})

    events = _steps(level, RIGHT, 3)

    assert [event.status for event in events] == [PLAYING, PLAYING, DIED]


# TC-090
def test_level_lets_the_player_stomp_an_enemy_by_falling_on_it() -> None:
    level = _level({(3, 10): "P", (3, 13): "W"})

    steps_taken = 0
    while level.enemies and steps_taken < 30:
        level.step(NONE, DT)
        steps_taken += 1

    state = (steps_taken, level.status, level.player.body.vy, level.player.body.box.y)
    assert state == (16, PLAYING, pytest.approx(-200), pytest.approx(192))


# TC-091
@pytest.mark.parametrize(
    ("camera_x", "player_x", "expected"),
    [(100, 87.9, DIED), (100, 88.0, DIED), (100, 88.1, PLAYING), (0, 0, PLAYING)],
)
def test_level_kills_the_player_who_leaves_the_screen_on_the_left(
    camera_x: float, player_x: float, expected: LevelStatus
) -> None:
    level = _level({(2, 13): "P", (10, 13): "W"})
    level.camera_x = camera_x
    level.player.body.box.x = player_x

    events = level.step(NONE, DT)

    assert events.status is expected


# TC-120
def test_level_prefers_death_when_the_player_touches_the_flag_and_leaves_the_screen() -> None:
    level = _level({(2, 13): "P", (5, 12): "F", (5, 13): "F"})
    level.camera_x = 100
    level.player.body.box.x = 88

    events = level.step(NONE, DT)

    assert events.status is DIED


# TC-121
def test_level_does_not_advance_after_it_is_cleared() -> None:
    level = _clearable_level()
    _steps(level, RIGHT, 5)
    x_before = level.player.body.box.x

    events = level.step(RIGHT, DT)

    assert (events.status, events.coins_gained, level.player.body.box.x) == (CLEARED, 0, x_before)


# TC-122
def test_level_updates_the_camera_on_the_frame_the_player_dies() -> None:
    level = _level({(20, 13): "P"}, ground=False)
    _steps(level, NONE, 15)
    level.camera_x = 0

    events = level.step(NONE, DT)

    assert (events.status, level.camera_x) == (DIED, pytest.approx(200))
