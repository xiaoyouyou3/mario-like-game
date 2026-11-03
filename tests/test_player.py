"""DES-007 player のテスト。"""

from __future__ import annotations

import pytest

from src.game.input_state import InputState
from src.game.player import Player, create_player, update_player
from src.game.stage_data import parse_stage
from src.game.tilemap import TileMap
from tests.conftest import stage_text

DT = 1 / 60
NONE = InputState(left=False, right=False, run=False, jump_pressed=False)
RIGHT = InputState(left=False, right=True, run=False, jump_pressed=False)
LEFT = InputState(left=True, right=False, run=False, jump_pressed=False)
BOTH = InputState(left=True, right=True, run=False, jump_pressed=False)
RUN_RIGHT = InputState(left=False, right=True, run=True, jump_pressed=False)
JUMP = InputState(left=False, right=False, run=False, jump_pressed=True)


def _map(cells: dict[tuple[int, int], str] | None = None, *, ground: bool = True) -> TileMap:
    return TileMap(parse_stage(stage_text(cells, ground=ground)))


def _ground_player(x: float = 50.0, vx: float = 0.0) -> Player:
    player = create_player(x, 208.0)
    player.body.on_ground = True
    player.body.vx = vx
    return player


def _air_player(vx: float = 0.0, vy: float = 0.0) -> Player:
    player = create_player(50.0, 100.0)
    player.body.vx = vx
    player.body.vy = vy
    return player


def _repeat(player: Player, inp: InputState, tilemap: TileMap, times: int) -> None:
    for _ in range(times):
        update_player(player, inp, tilemap, DT)


# TC-036
def test_update_player_accelerates_to_the_right_by_12_per_step() -> None:
    player = _ground_player()

    update_player(player, RIGHT, _map(), DT)

    assert player.body.vx == pytest.approx(12)


# TC-037
@pytest.mark.parametrize(("vx", "times"), [(0, 30), (84, 1), (90, 1)])
def test_update_player_caps_walking_speed_at_90(vx: float, times: int) -> None:
    player = _ground_player(vx=vx)

    _repeat(player, RIGHT, _map(), times)

    assert player.body.vx == pytest.approx(90)


# TC-038
def test_update_player_accelerates_to_the_left_by_12_per_step() -> None:
    player = _ground_player()

    update_player(player, LEFT, _map(), DT)

    assert player.body.vx == pytest.approx(-12)


# TC-039
@pytest.mark.parametrize(("vx", "expected"), [(0, 0), (60, 45)])
def test_update_player_treats_left_and_right_together_as_no_input(vx: float, expected: float) -> None:
    player = _ground_player(vx=vx)

    update_player(player, BOTH, _map(), DT)

    assert player.body.vx == pytest.approx(expected)


# TC-040
def test_update_player_slows_down_when_the_opposite_direction_is_held() -> None:
    player = _ground_player(vx=60)

    update_player(player, LEFT, _map(), DT)

    assert player.body.vx == pytest.approx(48)


# TC-041
def test_update_player_caps_running_speed_at_150() -> None:
    player = _ground_player()

    _repeat(player, RUN_RIGHT, _map(), 60)

    assert player.body.vx == pytest.approx(150)


# TC-042
def test_update_player_decelerates_on_the_ground_by_15_per_step() -> None:
    player = _ground_player(vx=90)

    update_player(player, NONE, _map(), DT)

    assert player.body.vx == pytest.approx(75)


# TC-043
@pytest.mark.parametrize(("times", "expected"), [(5, 15), (6, 0), (7, 0)])
def test_update_player_stops_at_zero_without_reversing(times: int, expected: float) -> None:
    player = _ground_player(vx=90)

    _repeat(player, NONE, _map(), times)

    assert player.body.vx == pytest.approx(expected)


# TC-044
def test_update_player_comes_to_rest_within_the_same_time_it_accelerated() -> None:
    player = _ground_player()
    tilemap = _map()
    _repeat(player, RIGHT, tilemap, 30)

    _repeat(player, NONE, tilemap, 30)

    assert player.body.vx == pytest.approx(0)


# TC-045
def test_update_player_decelerates_in_the_air_by_6_per_step() -> None:
    player = _air_player(vx=90)

    update_player(player, NONE, _map(ground=False), DT)

    assert player.body.vx == pytest.approx(84)


# TC-046
def test_update_player_starts_a_jump_from_the_ground() -> None:
    player = _ground_player()

    update_player(player, JUMP, _map(), DT)

    state = (player.body.vy, player.body.box.y, player.body.on_ground)
    assert state == (pytest.approx(-330), pytest.approx(202.5), False)


# TC-047
@pytest.mark.parametrize(("vy", "expected"), [(-100, -85), (100, 115)])
def test_update_player_ignores_jump_presses_in_the_air(vy: float, expected: float) -> None:
    player = _air_player(vy=vy)

    update_player(player, JUMP, _map(ground=False), DT)

    assert player.body.vy == pytest.approx(expected)


# TC-048
@pytest.mark.parametrize("press_every_step", [False, True])
def test_a_jump_rises_63_25_px(press_every_step: bool) -> None:
    player = _ground_player()
    tilemap = _map()

    highest = player.body.box.y
    for step in range(40):
        pressed = press_every_step or step == 0
        update_player(player, JUMP if pressed else NONE, tilemap, DT)
        highest = min(highest, player.body.box.y)

    assert highest == pytest.approx(144.75)


# TC-049
def test_update_player_leaves_the_ground_after_walking_off_a_ledge() -> None:
    floor = {(col, 14): "#" for col in range(6)}
    tilemap = _map(floor, ground=False)
    player = _ground_player(x=84)
    _repeat(player, RIGHT, tilemap, 12)
    after_12 = (player.body.on_ground, player.body.vy, player.body.box.y)

    update_player(player, RIGHT, tilemap, DT)

    assert (after_12, player.body.vy) == (
        (False, pytest.approx(15), pytest.approx(208.25)),
        pytest.approx(30),
    )


# TC-115
def test_update_player_does_not_jump_without_a_jump_press() -> None:
    player = _ground_player()

    update_player(player, NONE, _map(), DT)

    state = (player.body.vy, player.body.box.y, player.body.on_ground)
    assert state == (0, pytest.approx(208), True)


# TC-117
def test_update_player_accelerates_in_the_air_by_12_per_step() -> None:
    player = _air_player()

    update_player(player, RIGHT, _map(ground=False), DT)

    assert player.body.vx == pytest.approx(12)


# TC-118
@pytest.mark.parametrize(("vx", "expected"), [(150, 135), (92, 90)])
def test_update_player_slows_down_to_walking_speed_after_running(vx: float, expected: float) -> None:
    player = _ground_player(vx=vx)

    update_player(player, RIGHT, _map(), DT)

    assert player.body.vx == pytest.approx(expected)
