"""DES-013 hud のテスト。"""

from __future__ import annotations

import pytest

from src.game.hud import HudText, build_hud
from src.game.session import GameSession
from src.game.stage_data import parse_stage
from tests.conftest import stage_text


# TC-104, TC-105
@pytest.mark.parametrize(
    ("lives", "coins", "score", "expected"),
    [
        (3, 0, 0, HudText(lives="LIFE 3", coins="COIN 0", score="SCORE 0")),
        (2, 12, 1200, HudText(lives="LIFE 2", coins="COIN 12", score="SCORE 1200")),
    ],
)
def test_build_hud_formats_lives_coins_and_score_without_padding(
    lives: int, coins: int, score: int, expected: HudText
) -> None:
    session = GameSession(parse_stage(stage_text()))
    session.lives, session.coins, session.score = lives, coins, score

    hud = build_hud(session)

    assert hud == expected
