"""DES-009 interactions のテスト。"""

from __future__ import annotations

import pytest

from src.game.enemy import Enemy, EnemyKind, EnemyState, create_enemy
from src.game.interactions import resolve_player_enemies, resolve_shells_vs_walkers
from src.game.player import Player, create_player


def _walker(x: float = 100, y: float = 208) -> Enemy:
    return create_enemy(EnemyKind.WALKER, x, y)


def _koopa(x: float = 100, state: EnemyState = EnemyState.WALKING) -> Enemy:
    enemy = create_enemy(EnemyKind.KOOPA, x, 208)
    enemy.state = state
    return enemy


def _player(x: float, y: float, vy: float = 0.0) -> Player:
    player = create_player(x, y)
    player.body.vy = vy
    return player


# TC-063
def test_a_falling_player_stomps_a_walker_in_its_upper_half() -> None:
    enemy = _walker()
    player = _player(102, 196, vy=100)

    result = resolve_player_enemies(player, [enemy])

    assert (enemy.alive, result.player_died) == (False, False)


# TC-064
@pytest.mark.parametrize(("y", "stomped"), [(199.9, True), (200.0, True), (200.1, False)])
def test_stomp_zone_ends_at_the_enemy_midline(y: float, stomped: bool) -> None:
    enemy = _walker()
    player = _player(102, y, vy=100)

    result = resolve_player_enemies(player, [enemy])

    assert (enemy.alive, result.player_died) == (not stomped, not stomped)


# TC-065
@pytest.mark.parametrize("vy", [0, -50])
def test_a_player_that_is_not_falling_does_not_stomp(vy: float) -> None:
    enemy = _walker()
    player = _player(102, 196, vy=vy)

    result = resolve_player_enemies(player, [enemy])

    assert (enemy.alive, result.player_died) == (True, True)


# TC-066
def test_a_stomp_bounces_the_player_and_rests_it_on_the_enemy() -> None:
    player = _player(102, 196, vy=100)

    resolve_player_enemies(player, [_walker()])

    assert (player.body.vy, player.body.box.y) == (pytest.approx(-200), pytest.approx(192))


# TC-067
def test_stomping_a_walking_koopa_turns_it_into_an_idle_shell() -> None:
    enemy = _koopa()
    player = _player(102, 196, vy=100)

    result = resolve_player_enemies(player, [enemy])

    state = (enemy.state, enemy.body.vx, enemy.alive, result.player_died, player.body.vy)
    assert state == (EnemyState.SHELL_IDLE, 0, True, False, pytest.approx(-200))


# TC-068
@pytest.mark.parametrize("x", [90, 110])
@pytest.mark.parametrize("kind", [EnemyKind.WALKER, EnemyKind.KOOPA])
def test_touching_a_walking_enemy_from_the_side_kills_the_player(kind: EnemyKind, x: float) -> None:
    enemy = create_enemy(kind, 100, 208)
    player = _player(x, 208)

    result = resolve_player_enemies(player, [enemy])

    assert (result.player_died, enemy.alive) == (True, True)


# TC-069
def test_touching_a_walking_enemy_from_below_kills_the_player() -> None:
    player = _player(102, 218, vy=-50)

    result = resolve_player_enemies(player, [_walker()])

    assert result.player_died is True


# TC-070
@pytest.mark.parametrize("x", [60, 88])
def test_a_player_that_does_not_overlap_an_enemy_is_unaffected(x: float) -> None:
    enemy = _walker()
    player = _player(x, 208)

    result = resolve_player_enemies(player, [enemy])

    assert (result.player_died, enemy.alive, player.body.vy) == (False, True, 0)


# TC-071
def test_a_removed_enemy_is_ignored() -> None:
    enemy = _walker()
    enemy.alive = False
    player = _player(90, 208)

    result = resolve_player_enemies(player, [enemy])

    assert result.player_died is False


# TC-072
@pytest.mark.parametrize("a_first", [True, False])
def test_stomps_are_resolved_before_death_contacts_regardless_of_list_order(a_first: bool) -> None:
    a = _walker(100, 208)
    b = _walker(112, 196)
    player = _player(108, 196, vy=100)

    result = resolve_player_enemies(player, [a, b] if a_first else [b, a])

    assert (a.alive, b.alive, result.player_died) == (False, True, True)


# TC-073
@pytest.mark.parametrize(
    ("x", "y", "vy", "direction", "vx"),
    [(90, 208, 0, 1, 200), (110, 208, 0, -1, -200), (102, 196, 100, 1, 200)],
)
def test_touching_an_idle_shell_kicks_it_away_without_bouncing_the_player(
    x: float, y: float, vy: float, direction: int, vx: float
) -> None:
    shell = _koopa(state=EnemyState.SHELL_IDLE)
    player = _player(x, y, vy=vy)

    result = resolve_player_enemies(player, [shell])

    state = (shell.state, shell.direction, shell.body.vx, result.player_died)
    assert (state, player.body.vy, player.body.box.y) == (
        (EnemyState.SHELL_SLIDING, direction, vx, False),
        vy,
        y,
    )


# TC-074
def test_stomping_a_sliding_shell_stops_it() -> None:
    shell = _koopa(state=EnemyState.SHELL_SLIDING)
    shell.slide_age = 30
    shell.body.vx = 200
    player = _player(102, 196, vy=100)

    result = resolve_player_enemies(player, [shell])

    state = (shell.state, shell.body.vx, result.player_died, player.body.vy)
    assert state == (EnemyState.SHELL_IDLE, 0, False, pytest.approx(-200))


# TC-075
@pytest.mark.parametrize(
    ("slide_age", "died"),
    [(0, False), (11, False), (12, False), (13, True), (14, True), (100, True)],
)
def test_a_sliding_shell_is_harmless_only_during_its_grace_frames(
    slide_age: int, died: bool
) -> None:
    shell = _koopa(state=EnemyState.SHELL_SLIDING)
    shell.slide_age = slide_age
    player = _player(90, 208)

    result = resolve_player_enemies(player, [shell])

    assert result.player_died is died


# TC-076
@pytest.mark.parametrize("shell_first", [True, False])
def test_a_sliding_shell_kills_a_walker_it_touches(shell_first: bool) -> None:
    shell = _koopa(state=EnemyState.SHELL_SLIDING)
    walker = _walker(110, 208)

    resolve_shells_vs_walkers([shell, walker] if shell_first else [walker, shell])

    assert (walker.alive, shell.state) == (False, EnemyState.SHELL_SLIDING)


# TC-077
@pytest.mark.parametrize(
    ("first", "second"),
    [
        (EnemyState.SHELL_SLIDING, EnemyState.WALKING),
        (EnemyState.SHELL_SLIDING, EnemyState.SHELL_IDLE),
        (EnemyState.SHELL_IDLE, None),
    ],
)
def test_only_a_sliding_shell_touching_a_walker_kills_anything(
    first: EnemyState, second: EnemyState | None
) -> None:
    a = _koopa(100, first)
    b = _koopa(110, second) if second is not None else _walker(110, 208)
    before = (a.state, b.state)

    resolve_shells_vs_walkers([a, b])

    assert (a.alive, b.alive, (a.state, b.state)) == (True, True, before)


# TC-119
@pytest.mark.parametrize(("x", "y"), [(70, 196), (102, 192)])
def test_a_player_that_only_touches_or_misses_an_enemy_does_not_stomp(x: float, y: float) -> None:
    enemy = _walker()
    player = _player(x, y, vy=100)

    result = resolve_player_enemies(player, [enemy])

    assert (result.player_died, enemy.alive, player.body.vy) == (False, True, 100)


# TC-119
def test_a_player_overlapping_by_a_tenth_of_a_pixel_stomps() -> None:
    enemy = _walker()
    player = _player(102, 192.1, vy=100)

    result = resolve_player_enemies(player, [enemy])

    assert (enemy.alive, result.player_died) == (False, False)
