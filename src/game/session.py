"""画面遷移・残機・コイン・スコアを持つセッション。"""

from __future__ import annotations

from enum import Enum

from src.game.constants import COIN_SCORE, INITIAL_LIVES
from src.game.input_state import InputState
from src.game.level import Level, LevelStatus
from src.game.stage_data import StageData


class Screen(Enum):
    TITLE = 0
    PLAYING = 1
    CLEAR = 2
    GAME_OVER = 3


class GameSession:
    def __init__(self, stage: StageData) -> None:
        self._stage = stage
        self.screen = Screen.TITLE
        self.lives = INITIAL_LIVES
        self.coins = 0
        self.score = 0
        self.level: Level | None = None

    def update(self, inp: InputState, dt: float) -> None:
        """TITLE / CLEAR / GAME_OVER では jump_pressed だけを見る。PLAYING では Level.step の結果を反映する。"""
        if self.screen is Screen.PLAYING:
            self._update_playing(inp, dt)
        elif inp.jump_pressed:
            self._leave_screen()

    def _leave_screen(self) -> None:
        if self.screen is Screen.TITLE:
            self.lives = INITIAL_LIVES
            self.coins = 0
            self.score = 0
            self.level = Level(self._stage)
            self.screen = Screen.PLAYING
        else:
            self.screen = Screen.TITLE

    def _update_playing(self, inp: InputState, dt: float) -> None:
        if self.level is None:
            return
        events = self.level.step(inp, dt)
        self.coins += events.coins_gained
        self.score += events.coins_gained * COIN_SCORE
        if events.status is LevelStatus.PLAYER_DIED:
            self.lives -= 1
            if self.lives > 0:
                self.level = Level(self._stage)
            else:
                self.screen = Screen.GAME_OVER
        elif events.status is LevelStatus.CLEARED:
            self.screen = Screen.CLEAR
