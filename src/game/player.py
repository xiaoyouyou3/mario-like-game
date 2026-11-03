"""プレイヤーの速度と位置の更新。"""

from __future__ import annotations

import math
from dataclasses import dataclass

from src.game.constants import (
    ACCEL,
    AIR_DECEL,
    GROUND_DECEL,
    JUMP_SPEED,
    PLAYER_H,
    PLAYER_W,
    RUN_MAX_SPEED,
    WALK_MAX_SPEED,
)
from src.game.geometry import Aabb
from src.game.input_state import InputState
from src.game.physics import Body, CollisionResult, apply_gravity, move_and_collide
from src.game.tilemap import TileMap


@dataclass
class Player:
    body: Body
    alive: bool = True


def create_player(x: float, y: float) -> Player:
    return Player(body=Body(Aabb(x, y, PLAYER_W, PLAYER_H)))


def _horizontal_speed(
    vx: float, direction: int, max_speed: float, decel: float, dt: float
) -> float:
    """入力方向 direction（-1, 0, +1）に応じた次の vx。"""
    if direction == 0:
        return math.copysign(max(abs(vx) - decel * dt, 0.0), vx)
    if vx * direction <= 0 or abs(vx) <= max_speed:
        return max(-max_speed, min(max_speed, vx + direction * ACCEL * dt))
    return math.copysign(max(abs(vx) - decel * dt, max_speed), vx)


def update_player(
    player: Player, inp: InputState, tilemap: TileMap, dt: float
) -> CollisionResult:
    body = player.body
    direction = int(inp.right) - int(inp.left)
    max_speed = RUN_MAX_SPEED if inp.run else WALK_MAX_SPEED
    decel = GROUND_DECEL if body.on_ground else AIR_DECEL
    body.vx = _horizontal_speed(body.vx, direction, max_speed, decel, dt)
    if body.on_ground and inp.jump_pressed:
        body.vy = -JUMP_SPEED
    apply_gravity(body, dt)
    return move_and_collide(body, tilemap, dt)
