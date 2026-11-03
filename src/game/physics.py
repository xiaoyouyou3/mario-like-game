"""重力の適用と、軸を分けたタイル衝突の解決。"""

from __future__ import annotations

from dataclasses import dataclass

from src.game.constants import FALL_MAX_SPEED, GRAVITY, TILE_SIZE
from src.game.geometry import Aabb, tile_span
from src.game.tilemap import TileMap


@dataclass
class Body:
    box: Aabb
    vx: float = 0.0
    vy: float = 0.0
    on_ground: bool = False


@dataclass(frozen=True)
class CollisionResult:
    hit_left: bool
    hit_right: bool
    hit_ceiling: bool
    ceiling_cell: tuple[int, int] | None


def apply_gravity(body: Body, dt: float) -> None:
    body.vy = min(body.vy + GRAVITY * dt, FALL_MAX_SPEED)


def _solid_cells(box: Aabb, tilemap: TileMap) -> list[tuple[int, int]]:
    """box と重なる固体タイルの (col, row) を返す。"""
    return [
        (col, row)
        for row in tile_span(box.top, box.bottom)
        for col in tile_span(box.left, box.right)
        if tilemap.is_solid(col, row)
    ]


def _resolve_x(body: Body, tilemap: TileMap) -> tuple[bool, bool]:
    cells = _solid_cells(body.box, tilemap)
    if not cells:
        return False, False
    cols = [col for col, _ in cells]
    if body.vx > 0:
        body.box.x = min(cols) * TILE_SIZE - body.box.w
        body.vx = 0.0
        return False, True
    if body.vx < 0:
        body.box.x = (max(cols) + 1) * TILE_SIZE
        body.vx = 0.0
        return True, False
    return False, False


def _nearest_cell(cells: list[tuple[int, int]], center_x: float) -> tuple[int, int]:
    """center_x に最も近いタイルの中心を持つセル。同距離なら列番号が小さい方。"""
    return min(
        cells, key=lambda cell: (abs((cell[0] + 0.5) * TILE_SIZE - center_x), cell[0])
    )


def _resolve_y(body: Body, tilemap: TileMap) -> tuple[bool, tuple[int, int] | None]:
    """y 方向を解決する。戻り値は (着地したか, 天井セル)。"""
    cells = _solid_cells(body.box, tilemap)
    if not cells or body.vy == 0:
        return False, None
    rows = [row for _, row in cells]
    if body.vy > 0:
        body.box.y = min(rows) * TILE_SIZE - body.box.h
        body.vy = 0.0
        return True, None
    lowest = max(rows)
    body.box.y = (lowest + 1) * TILE_SIZE
    body.vy = 0.0
    ceiling = [cell for cell in cells if cell[1] == lowest]
    return False, _nearest_cell(ceiling, body.box.center_x)


def move_and_collide(body: Body, tilemap: TileMap, dt: float) -> CollisionResult:
    body.box.x += body.vx * dt
    hit_left, hit_right = _resolve_x(body, tilemap)
    body.box.y += body.vy * dt
    landed, ceiling_cell = _resolve_y(body, tilemap)
    body.on_ground = landed
    return CollisionResult(hit_left, hit_right, ceiling_cell is not None, ceiling_cell)
