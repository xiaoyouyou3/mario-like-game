"""DES-008 enemy のテスト。"""

from __future__ import annotations

import pytest

from src.game.enemy import (
    Enemy,
    EnemyKind,
    EnemyState,
    create_enemy,
    kick_shell,
    stomp_enemy,
    update_enemy,
)
from src.game.geometry import Aabb
from src.game.stage_data import parse_stage
from src.game.tilemap import TileMap
from tests.conftest import stage_text

DT = 1 / 60
WALL_LEFT = {(5, 12): "#", (5, 13): "#"}
WALL_RIGHT = {(10, 12): "#", (10, 13): "#"}


def _map(cells: dict[tuple[int, int], str] | None = None, *, ground: bool = True) -> TileMap:
    return TileMap(parse_stage(stage_text(cells, ground=ground)))


def _floor(first_col: int, last_col: int) -> dict[tuple[int, int], str]:
    return {(col, 14): "#" for col in range(first_col, last_col + 1)}


def _ground_enemy(
    kind: EnemyKind,
    x: float,
    *,
    state: EnemyState = EnemyState.WALKING,
    direction: int = -1,
) -> Enemy:
    enemy = create_enemy(kind, x, 208.0)
    enemy.body.on_ground = True
    enemy.state = state
    enemy.direction = direction
    return enemy


# TC-050
@pytest.mark.parametrize("kind", [EnemyKind.WALKER, EnemyKind.KOOPA])
def test_create_enemy_starts_walking_to_the_left(kind: EnemyKind) -> None:
    enemy = create_enemy(kind, 100, 208)

    state = (enemy.state, enemy.direction, enemy.alive, enemy.body.box)
    assert state == (EnemyState.WALKING, -1, True, Aabb(100, 208, 16, 16))


# TC-051
@pytest.mark.parametrize("kind", [EnemyKind.WALKER, EnemyKind.KOOPA])
@pytest.mark.parametrize(("direction", "vx", "x"), [(-1, -30, 99.5), (1, 30, 100.5)])
def test_update_enemy_walks_at_30_in_its_direction(
    kind: EnemyKind, direction: int, vx: float, x: float
) -> None:
    enemy = _ground_enemy(kind, 100, direction=direction)

    update_enemy(enemy, _map(), DT)

    assert (enemy.body.vx, enemy.body.box.x) == (pytest.approx(vx), pytest.approx(x))


# TC-052
def test_update_enemy_settles_onto_the_floor() -> None:
    enemy = create_enemy(EnemyKind.WALKER, 100, 207.9)

    update_enemy(enemy, _map(), DT)

    assert (enemy.body.box.y, enemy.body.on_ground) == (pytest.approx(208), True)


# TC-053
def test_update_enemy_keeps_an_idle_shell_still() -> None:
    enemy = _ground_enemy(EnemyKind.KOOPA, 100, state=EnemyState.SHELL_IDLE)

    for _ in range(10):
        update_enemy(enemy, _map(), DT)

    assert (enemy.body.box.x, enemy.body.vx) == (pytest.approx(100), 0)


# TC-054
@pytest.mark.parametrize(
    ("state", "expected"),
    [(EnemyState.SHELL_SLIDING, 3), (EnemyState.WALKING, 0), (EnemyState.SHELL_IDLE, 0)],
)
def test_update_enemy_counts_slide_frames_only_while_sliding(
    state: EnemyState, expected: int
) -> None:
    enemy = _ground_enemy(EnemyKind.KOOPA, 100, state=state)

    for _ in range(3):
        update_enemy(enemy, _map(), DT)

    assert enemy.slide_age == expected


# TC-055
@pytest.mark.parametrize(
    ("wall", "x", "direction", "expected"),
    [
        (WALL_LEFT, 96.2, -1, (96, 1, 30)),
        (WALL_RIGHT, 143.8, 1, (144, -1, -30)),
    ],
)
def test_update_enemy_turns_around_at_a_wall(
    wall: dict[tuple[int, int], str],
    x: float,
    direction: int,
    expected: tuple[float, int, float],
) -> None:
    enemy = _ground_enemy(EnemyKind.WALKER, x, direction=direction)

    update_enemy(enemy, _map(wall), DT)

    actual = (enemy.body.box.x, enemy.direction, enemy.body.vx)
    assert actual == (pytest.approx(expected[0]), expected[1], pytest.approx(expected[2]))


# TC-056
@pytest.mark.parametrize(
    ("kind", "x", "expected"),
    [
        (EnemyKind.WALKER, 142.9, (1, 143.4)),
        (EnemyKind.WALKER, 143.0, (-1, 142.5)),
        (EnemyKind.KOOPA, 143.0, (-1, 142.5)),
    ],
)
def test_update_enemy_turns_around_before_a_cliff_on_the_right(
    kind: EnemyKind, x: float, expected: tuple[int, float]
) -> None:
    enemy = _ground_enemy(kind, x, direction=1)

    update_enemy(enemy, _map(_floor(0, 9), ground=False), DT)

    actual = (enemy.direction, enemy.body.box.x, enemy.body.on_ground)
    assert actual == (expected[0], pytest.approx(expected[1]), True)


# TC-057
@pytest.mark.parametrize(("x", "expected"), [(161.0, (-1, 160.5)), (160.9, (1, 161.4))])
def test_update_enemy_turns_around_before_a_cliff_on_the_left(
    x: float, expected: tuple[int, float]
) -> None:
    enemy = _ground_enemy(EnemyKind.WALKER, x, direction=-1)

    update_enemy(enemy, _map(_floor(10, 19), ground=False), DT)

    assert (enemy.direction, enemy.body.box.x) == (expected[0], pytest.approx(expected[1]))


# TC-058
@pytest.mark.parametrize(
    ("wall", "x", "direction", "expected"),
    [
        (WALL_LEFT, 96.5, -1, (96, 1, 200)),
        (WALL_RIGHT, 143.5, 1, (144, -1, -200)),
    ],
)
def test_update_enemy_turns_a_sliding_shell_around_at_a_wall(
    wall: dict[tuple[int, int], str],
    x: float,
    direction: int,
    expected: tuple[float, int, float],
) -> None:
    enemy = _ground_enemy(EnemyKind.KOOPA, x, state=EnemyState.SHELL_SLIDING, direction=direction)

    update_enemy(enemy, _map(wall), DT)

    actual = (enemy.body.box.x, enemy.direction, enemy.body.vx)
    assert actual == (pytest.approx(expected[0]), expected[1], pytest.approx(expected[2]))


# TC-059
def test_update_enemy_lets_a_sliding_shell_fall_off_a_ledge() -> None:
    enemy = _ground_enemy(EnemyKind.KOOPA, 157, state=EnemyState.SHELL_SLIDING, direction=1)

    update_enemy(enemy, _map(_floor(0, 9), ground=False), DT)

    state = (enemy.direction, enemy.body.vx, enemy.body.on_ground, enemy.body.vy)
    assert state == (1, pytest.approx(200), False, pytest.approx(15))


# TC-060
def test_stomp_enemy_removes_a_walker() -> None:
    enemy = _ground_enemy(EnemyKind.WALKER, 100)

    stomp_enemy(enemy)

    assert enemy.alive is False


# TC-061
@pytest.mark.parametrize(
    ("state", "slide_age", "vx"),
    [(EnemyState.WALKING, 0, -30), (EnemyState.SHELL_SLIDING, 30, 200)],
)
def test_stomp_enemy_turns_a_koopa_into_an_idle_shell(
    state: EnemyState, slide_age: int, vx: float
) -> None:
    enemy = _ground_enemy(EnemyKind.KOOPA, 100, state=state)
    enemy.slide_age = slide_age
    enemy.body.vx = vx

    stomp_enemy(enemy)

    result = (enemy.state, enemy.body.vx, enemy.slide_age, enemy.alive)
    assert result == (EnemyState.SHELL_IDLE, 0, 0, True)


# TC-062
@pytest.mark.parametrize(
    ("player_center_x", "direction", "vx"),
    [(96, 1, 200), (120, -1, -200), (108, 1, 200)],
)
def test_kick_shell_slides_away_from_the_player(
    player_center_x: float, direction: int, vx: float
) -> None:
    enemy = _ground_enemy(EnemyKind.KOOPA, 100, state=EnemyState.SHELL_IDLE)

    kick_shell(enemy, player_center_x)

    result = (enemy.direction, enemy.body.vx, enemy.state, enemy.slide_age)
    assert result == (direction, vx, EnemyState.SHELL_SLIDING, 0)
