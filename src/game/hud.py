"""HUD に表示する文字列。"""

from __future__ import annotations

from dataclasses import dataclass

from src.game.session import GameSession


@dataclass(frozen=True)
class HudText:
    lives: str
    coins: str
    score: str


def build_hud(session: GameSession) -> HudText:
    return HudText(
        lives=f"LIFE {session.lives}",
        coins=f"COIN {session.coins}",
        score=f"SCORE {session.score}",
    )
