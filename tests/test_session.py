"""DES-012 session のテスト。"""

from __future__ import annotations

import pytest

from src.game.input_state import InputState
from src.game.session import GameSession, Screen
from src.game.stage_data import StageData, TileKind, parse_stage
from tests.conftest import stage_text

DT = 1 / 60
NONE = InputState(left=False, right=False, run=False, jump_pressed=False)
RIGHT = InputState(left=False, right=True, run=False, jump_pressed=False)
JUMP = InputState(left=False, right=False, run=False, jump_pressed=True)
HELD_ONLY = InputState(left=True, right=True, run=True, jump_pressed=False)


def _stage(cells: dict[tuple[int, int], str] | None = None) -> StageData:
    return parse_stage(stage_text(cells, ground=True))


def _playing(cells: dict[tuple[int, int], str] | None = None) -> GameSession:
    session = GameSession(_stage(cells))
    session.update(JUMP, DT)
    return session


def _grounded(cells: dict[tuple[int, int], str] | None = None) -> GameSession:
    session = _playing(cells)
    session.update(NONE, DT)
    return session


def _block_stage_session_after_one_hit() -> GameSession:
    """? ブロックを叩いて USED にし、敵が歩いたあと、カメラを 200 にした PLAYING の Session。"""
    session = _grounded({(2, 13): "P", (10, 13): "W", (2, 12): "?"})
    session.update(JUMP, DT)
    session.update(NONE, DT)
    session.update(NONE, DT)
    assert session.level is not None
    assert session.level.enemies[0].body.box.x < 160  # 敵が歩いて初期位置から動いている
    session.level.camera_x = 200
    return session


# TC-092
def test_a_new_session_starts_on_the_title_screen() -> None:
    session = GameSession(_stage())

    assert session.screen is Screen.TITLE


# TC-093
def test_pressing_jump_on_the_title_starts_play_with_initial_values() -> None:
    session = GameSession(_stage({(2, 13): "P"}))

    session.update(JUMP, DT)

    assert session.level is not None
    box = session.level.player.body.box
    state = (session.screen, session.lives, session.coins, session.score, (box.x, box.y))
    assert state == (Screen.PLAYING, 3, 0, 0, (34, 208))


# TC-094
def test_only_the_jump_press_starts_play() -> None:
    session = GameSession(_stage())

    for _ in range(5):
        session.update(HELD_ONLY, DT)

    assert session.screen is Screen.TITLE


# TC-095
@pytest.mark.parametrize("screen", [Screen.CLEAR, Screen.GAME_OVER])
@pytest.mark.parametrize(("inp", "expected_is_title"), [(JUMP, True), (NONE, False)])
def test_jump_returns_from_the_end_screens_to_the_title(
    screen: Screen, inp: InputState, expected_is_title: bool
) -> None:
    session = GameSession(_stage())
    session.screen = screen

    session.update(inp, DT)

    assert session.screen is (Screen.TITLE if expected_is_title else screen)


# TC-096
def test_starting_again_resets_lives_coins_and_score() -> None:
    session = GameSession(_stage())
    session.lives, session.coins, session.score = 0, 7, 900

    session.update(JUMP, DT)

    state = (session.lives, session.coins, session.score, session.screen)
    assert state == (3, 0, 0, Screen.PLAYING)


# TC-097
def test_a_coin_adds_one_to_coins_and_100_to_score() -> None:
    session = _grounded({(2, 13): "P", (2, 12): "?"})
    session.coins, session.score = 2, 500

    session.update(JUMP, DT)

    assert (session.coins, session.score) == (3, 600)


# TC-098
@pytest.mark.parametrize(("lives", "expected"), [(3, 2), (2, 1)])
def test_dying_with_lives_left_costs_one_life_and_keeps_playing(lives: int, expected: int) -> None:
    session = _grounded({(2, 13): "P"})
    session.lives = lives
    assert session.level is not None
    session.level.camera_x = 200

    session.update(NONE, DT)

    assert (session.lives, session.screen) == (expected, Screen.PLAYING)


# TC-099
def test_dying_restarts_the_player_at_the_start_position() -> None:
    session = _grounded({(2, 13): "P"})
    for _ in range(5):
        session.update(RIGHT, DT)
    assert session.level is not None
    assert session.level.player.body.box.x == pytest.approx(37)  # 右へ動いている
    session.level.camera_x = 200

    session.update(NONE, DT)

    assert session.level is not None
    box = session.level.player.body.box
    assert ((box.x, box.y), session.level.camera_x) == ((34, 208), 0)


# TC-100
def test_dying_restores_blocks_and_enemies() -> None:
    session = _block_stage_session_after_one_hit()

    session.update(NONE, DT)

    assert session.level is not None
    boxes = [(e.body.box.x, e.body.box.y, e.body.box.w, e.body.box.h) for e in session.level.enemies]
    assert (session.level.tilemap.tile_at(2, 12), boxes) == (TileKind.QUESTION, [(160, 208, 16, 16)])


# TC-101
def test_dying_keeps_the_coins_and_score_gained_before() -> None:
    session = _block_stage_session_after_one_hit()

    session.update(NONE, DT)

    assert (session.coins, session.score) == (1, 100)


# TC-102
def test_dying_on_the_last_life_ends_the_game() -> None:
    session = _grounded({(2, 13): "P"})
    session.lives = 1
    assert session.level is not None
    session.level.camera_x = 200

    session.update(NONE, DT)

    assert (session.lives, session.screen) == (0, Screen.GAME_OVER)


# TC-103
def test_reaching_the_flag_ends_play_with_the_clear_screen() -> None:
    flag = {(8, row): "F" for row in range(10, 14)}
    session = _playing({(7, 13): "P", **flag})

    screens = []
    for _ in range(5):
        session.update(RIGHT, DT)
        screens.append(session.screen)

    assert screens == [Screen.PLAYING] * 4 + [Screen.CLEAR]
