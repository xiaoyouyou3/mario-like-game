"""敵（歩く敵・甲羅の敵）の状態と更新。"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum

from src.game.constants import (
    ENEMY_H,
    ENEMY_W,
    ENEMY_WALK_SPEED,
    SHELL_SLIDE_SPEED,
    TILE_SIZE,
)
from src.game.geometry import Aabb
from src.game.physics import Body, apply_gravity, move_and_collide
from src.game.tilemap import TileMap


class EnemyKind(Enum):
    WALKER = 0
    KOOPA = 1


class EnemyState(Enum):
    WALKING = 0
    SHELL_IDLE = 1
    SHELL_SLIDING = 2


@dataclass
class Enemy:
    kind: EnemyKind
    state: EnemyState
    body: Body
    direction: int = -1
    slide_age: int = 0
    alive: bool = True


def create_enemy(kind: EnemyKind, x: float, y: float) -> Enemy:
    body = Body(Aabb(x, y, ENEMY_W, ENEMY_H))
    return Enemy(kind=kind, state=EnemyState.WALKING, body=body)


def _speed(enemy: Enemy) -> float:
    if enemy.state is EnemyState.WALKING:
        return ENEMY_WALK_SPEED
    if enemy.state is EnemyState.SHELL_SLIDING:
        return SHELL_SLIDE_SPEED
    return 0.0


def _floor_ahead(enemy: Enemy, tilemap: TileMap) -> bool:
    """進行方向の足元（端の外へ 1 px、下へ 1 px）が固体か。"""
    box = enemy.body.box
    probe_x = box.right + 1 if enemy.direction > 0 else box.left - 1
    col = math.floor(probe_x / TILE_SIZE)
    row = math.floor((box.bottom + 1) / TILE_SIZE)
    return tilemap.is_solid(col, row)


def update_enemy(enemy: Enemy, tilemap: TileMap, dt: float) -> None:
    body = enemy.body
    if (
        enemy.state is EnemyState.WALKING
        and body.on_ground
        and not _floor_ahead(enemy, tilemap)
    ):
        enemy.direction = -enemy.direction
    body.vx = enemy.direction * _speed(enemy)
    if enemy.state is EnemyState.SHELL_SLIDING:
        enemy.slide_age += 1
    apply_gravity(body, dt)
    result = move_and_collide(body, tilemap, dt)
    if result.hit_left or result.hit_right:
        enemy.direction = -enemy.direction
        body.vx = enemy.direction * _speed(enemy)


def stomp_enemy(enemy: Enemy) -> None:
    if enemy.kind is EnemyKind.WALKER:
        enemy.alive = False
    elif enemy.state is not EnemyState.SHELL_IDLE:
        enemy.state = EnemyState.SHELL_IDLE
        enemy.body.vx = 0.0
        enemy.slide_age = 0


def kick_shell(enemy: Enemy, player_center_x: float) -> None:
    enemy.direction = -1 if enemy.body.box.center_x < player_center_x else 1
    enemy.state = EnemyState.SHELL_SLIDING
    enemy.slide_age = 0
    enemy.body.vx = enemy.direction * SHELL_SLIDE_SPEED
