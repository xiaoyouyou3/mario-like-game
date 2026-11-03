"""1 ステージ分の状態と、1 ステップの更新。"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from src.game.camera import next_camera_x
from src.game.constants import (
    PLAYER_START_OFFSET_X,
    STAGE_H_TILES,
    STAGE_W_TILES,
    TILE_SIZE,
)
from src.game.enemy import Enemy, EnemyKind, create_enemy, update_enemy
from src.game.input_state import InputState
from src.game.interactions import (
    PlayerEnemyResult,
    resolve_player_enemies,
    resolve_shells_vs_walkers,
)
from src.game.player import create_player, update_player
from src.game.stage_data import StageData
from src.game.tilemap import TileMap

LEVEL_WIDTH = STAGE_W_TILES * TILE_SIZE  # px
STAGE_HEIGHT = STAGE_H_TILES * TILE_SIZE  # px


class LevelStatus(Enum):
    PLAYING = 0
    PLAYER_DIED = 1
    CLEARED = 2


@dataclass(frozen=True)
class LevelEvents:
    coins_gained: int
    status: LevelStatus


class Level:
    def __init__(self, data: StageData) -> None:
        start_col, start_row = data.start
        self.player = create_player(
            start_col * TILE_SIZE + PLAYER_START_OFFSET_X, start_row * TILE_SIZE
        )
        self.tilemap = TileMap(data)
        self.enemies: list[Enemy] = [
            create_enemy(EnemyKind.WALKER, col * TILE_SIZE, row * TILE_SIZE)
            for col, row in data.walkers
        ] + [
            create_enemy(EnemyKind.KOOPA, col * TILE_SIZE, row * TILE_SIZE)
            for col, row in data.koopas
        ]
        self.flag = data.flag
        self.camera_x = 0.0
        self.status = LevelStatus.PLAYING

    def step(self, inp: InputState, dt: float) -> LevelEvents:
        """status が PLAYING のときだけ進める。"""
        if self.status is not LevelStatus.PLAYING:
            return LevelEvents(coins_gained=0, status=self.status)
        coins = self._update_player_and_blocks(inp, dt)
        contact = self._update_enemies(dt)
        self.status = self._judge(contact.player_died)
        self.camera_x = next_camera_x(
            self.camera_x, self.player.body.box.center_x, LEVEL_WIDTH
        )
        return LevelEvents(coins_gained=coins, status=self.status)

    def _update_player_and_blocks(self, inp: InputState, dt: float) -> int:
        result = update_player(self.player, inp, self.tilemap, dt)
        if result.ceiling_cell is not None and self.tilemap.hit_question(
            *result.ceiling_cell
        ):
            return 1
        return 0

    def _update_enemies(self, dt: float) -> PlayerEnemyResult:
        for enemy in self.enemies:
            update_enemy(enemy, self.tilemap, dt)
            if enemy.body.box.top > STAGE_HEIGHT:
                enemy.alive = False
        resolve_shells_vs_walkers(self.enemies)
        contact = resolve_player_enemies(self.player, self.enemies)
        self.enemies = [enemy for enemy in self.enemies if enemy.alive]
        return contact

    def _judge(self, touched_deadly_enemy: bool) -> LevelStatus:
        """カメラ x は更新前の値を使う。死亡と旗が同時なら死亡を優先する。"""
        box = self.player.body.box
        if touched_deadly_enemy or box.top > STAGE_HEIGHT or box.right <= self.camera_x:
            return LevelStatus.PLAYER_DIED
        if box.overlaps(self.flag):
            return LevelStatus.CLEARED
        return LevelStatus.PLAYING
