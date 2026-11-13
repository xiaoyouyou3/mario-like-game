"""描画と表示倍率。"""

from __future__ import annotations

import pygame

from src.game.constants import (
    PANEL_H,
    PLAY_H,
    SCREEN_H,
    SCREEN_W,
    STAGE_H_TILES,
    STAGE_W_TILES,
    TILE_SIZE,
)
from src.game.enemy import Enemy, EnemyKind, EnemyState
from src.game.geometry import Aabb
from src.game.hud import build_hud
from src.game.level import Level
from src.game.session import GameSession, Screen
from src.game.stage_data import TileKind
from src.game.tilemap import TileMap
from src.render.assets import Assets
from src.render.touch_controls import default_layout


def compute_scale(window_w: int, window_h: int) -> float:
    """縦横比を保ってウィンドウに収まる最大の倍率（小数）。幅か高さが 0 なら 0.0。"""
    return min(window_w / SCREEN_W, window_h / SCREEN_H)


SKY = (92, 148, 252)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_FILL = (255, 255, 255, 90)
BUTTON_LABELS = (("left", "<"), ("right", ">"), ("run", "RUN"), ("jump", "JUMP"))
HUD_X = (4, 84, 164)  # px
HUD_Y = 4  # px


def _text(surface: pygame.Surface, assets: Assets, text: str, y: int) -> None:
    """画面の横中央に白い文字を置く。"""
    image = assets.font.render(text, False, WHITE)
    surface.blit(image, ((SCREEN_W - image.get_width()) // 2, y))


def _draw_tiles(
    surface: pygame.Surface, level: Level, assets: Assets, camera: int
) -> None:
    sprites = {
        TileKind.SOLID: assets.images["solid"],
        TileKind.QUESTION: assets.images["question"],
        TileKind.USED: assets.images["used"],
    }
    first = camera // TILE_SIZE
    last = (camera + SCREEN_W) // TILE_SIZE + 1
    for row in range(STAGE_H_TILES):
        for col in range(first, min(last, STAGE_W_TILES)):
            sprite = sprites.get(level.tilemap.tile_at(col, row))
            if sprite is not None:
                surface.blit(sprite, (col * TILE_SIZE - camera, row * TILE_SIZE))


def _draw_flag(
    surface: pygame.Surface, level: Level, assets: Assets, camera: int
) -> None:
    flag = level.flag
    for y in range(int(flag.top), int(flag.bottom), TILE_SIZE):
        surface.blit(assets.images["flag"], (int(flag.left) - camera, y))


def _enemy_sprite(enemy: Enemy, assets: Assets) -> pygame.Surface:
    if enemy.kind is EnemyKind.WALKER:
        return assets.images["walker"]
    if enemy.state is EnemyState.WALKING:
        return assets.images["koopa"]
    return assets.images["shell"]


def _draw_level_background(surface: pygame.Surface, level: Level, assets: Assets) -> None:
    camera = int(level.camera_x)
    _draw_tiles(surface, level, assets, camera)
    _draw_flag(surface, level, assets, camera)


def _draw_entities(surface: pygame.Surface, level: Level, assets: Assets) -> None:
    """敵とプレイヤー。クリップせず描くので、穴に落ちる間も操作パネルの高さまで見える。"""
    camera = int(level.camera_x)
    for enemy in level.enemies:
        box = enemy.body.box
        surface.blit(_enemy_sprite(enemy, assets), (int(box.x) - camera, int(box.y)))
    player_box = level.player.body.box
    surface.blit(
        assets.images["player"], (int(player_box.x) - camera, int(player_box.y))
    )


def _draw_hud(surface: pygame.Surface, session: GameSession, assets: Assets) -> None:
    hud = build_hud(session)
    for x, text in zip(HUD_X, (hud.lives, hud.coins, hud.score), strict=True):
        surface.blit(assets.font.render(text, False, WHITE), (x, HUD_Y))


def _draw_touch_buttons(surface: pygame.Surface, assets: Assets) -> None:
    layout = default_layout()
    for name, label in BUTTON_LABELS:
        box: Aabb = getattr(layout, name)
        button = pygame.Surface((int(box.w), int(box.h)), pygame.SRCALPHA)
        button.fill(BUTTON_FILL)
        image = assets.font.render(label, False, WHITE)
        button.blit(
            image,
            (
                (button.get_width() - image.get_width()) // 2,
                (button.get_height() - image.get_height()) // 2,
            ),
        )
        surface.blit(button, (int(box.x), int(box.y)))


def column_has_ground(tilemap: TileMap, col: int) -> bool:
    """最下段のマスが固体なら True。穴の列は False。"""
    return tilemap.is_solid(col, STAGE_H_TILES - 1)


def _draw_ground_column(surface: pygame.Surface, assets: Assets, x: int) -> None:
    tile = assets.images["solid"]
    for y in range(PLAY_H, SCREEN_H, TILE_SIZE):
        surface.blit(tile, (x, y))


def _draw_panel(surface: pygame.Surface, assets: Assets, level: Level | None) -> None:
    """操作パネルを列ごとに塗る。穴の列は黒。level が None なら全列を地面で塗る。"""
    if level is None:
        for x in range(0, SCREEN_W, TILE_SIZE):
            _draw_ground_column(surface, assets, x)
        return
    camera = int(level.camera_x)
    first = camera // TILE_SIZE
    last = min((camera + SCREEN_W) // TILE_SIZE + 1, STAGE_W_TILES)
    for col in range(first, last):
        x = col * TILE_SIZE - camera
        if column_has_ground(level.tilemap, col):
            _draw_ground_column(surface, assets, x)
        else:
            surface.fill(BLACK, pygame.Rect(x, PLAY_H, TILE_SIZE, PANEL_H))


def _draw_stage_area(
    surface: pygame.Surface, session: GameSession, assets: Assets
) -> None:
    if session.screen is Screen.PLAYING and session.level is not None:
        _draw_level_background(surface, session.level, assets)
        _draw_hud(surface, session, assets)
    elif session.screen is Screen.TITLE:
        _text(surface, assets, "MARIO-LIKE", 80)
        _text(surface, assets, "PRESS Z TO START", 120)
    elif session.screen is Screen.CLEAR:
        _text(surface, assets, "STAGE CLEAR", 80)
        _text(surface, assets, "PRESS Z", 120)
    else:
        _text(surface, assets, "GAME OVER", 80)
        _text(surface, assets, "PRESS Z", 120)


def draw(
    surface: pygame.Surface, session: GameSession, assets: Assets, touch_visible: bool
) -> None:
    """内部解像度の面に、現在の画面を描く。ステージ領域は y < PLAY_H にクリップする。"""
    playing = session.screen is Screen.PLAYING and session.level is not None
    level = session.level if playing else None
    surface.fill(SKY)
    surface.set_clip(pygame.Rect(0, 0, SCREEN_W, PLAY_H))
    _draw_stage_area(surface, session, assets)
    surface.set_clip(None)
    _draw_panel(surface, assets, level)
    if level is not None:
        _draw_entities(surface, level, assets)
    if touch_visible:
        _draw_touch_buttons(surface, assets)
