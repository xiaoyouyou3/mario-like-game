"""初期化・固定ステップのループ・ステージファイルの読み込み。"""

from __future__ import annotations

import asyncio
from dataclasses import replace
from pathlib import Path

import pygame

from src.game.constants import FIXED_DT, SCREEN_H, SCREEN_W
from src.game.input_state import make_input, merge_held
from src.game.session import GameSession
from src.game.stage_data import parse_stage
from src.render.assets import load_assets
from src.render.input_mapper import detect_touch_device, keys_to_held
from src.render.renderer import compute_scale, draw
from src.render.touch_controls import default_layout, points_to_held

ROOT = Path(__file__).resolve().parent.parent
STAGE_PATH = ROOT / "assets" / "stages" / "stage1.txt"
IMAGE_DIR = ROOT / "assets" / "images"
MAX_STEPS_PER_FRAME = 5
FPS = 60
INITIAL_WINDOW_SCALE = 1.5
MOUSE_POINT_ID = -1
BLACK = (0, 0, 0)

Points = dict[int, tuple[float, float]]


OUTSIDE = (-1.0, -1.0)  # 内部解像度の外（どのボタンにも当たらない）


def _view_size(window_size: tuple[int, int]) -> tuple[int, int]:
    """ウィンドウに表示される内部描画面の大きさ（縦横比を保った小数倍）。"""
    scale = compute_scale(*window_size)
    return (int(SCREEN_W * scale), int(SCREEN_H * scale))


def _to_internal(
    x: float, y: float, window_size: tuple[int, int], normalized: bool
) -> tuple[float, float]:
    """ウィンドウ上の座標を、内部解像度（592x304）の座標へ変換する。"""
    window_w, window_h = window_size
    scale = compute_scale(window_w, window_h)
    if scale <= 0:
        return OUTSIDE
    view_w, view_h = _view_size(window_size)
    px, py = (x * window_w, y * window_h) if normalized else (x, y)
    return (
        (px - (window_w - view_w) // 2) / scale,
        (py - (window_h - view_h) // 2) / scale,
    )


def _update_points(
    event: pygame.event.Event, points: Points, window_size: tuple[int, int]
) -> None:
    """タッチ（指）とマウスのボタン押下を、押している点の一覧に反映する。"""
    if event.type in (pygame.FINGERDOWN, pygame.FINGERMOTION):
        points[event.finger_id] = _to_internal(
            event.x, event.y, window_size, normalized=True
        )
    elif event.type == pygame.FINGERUP:
        points.pop(event.finger_id, None)
    elif event.type == pygame.MOUSEBUTTONDOWN or (
        event.type == pygame.MOUSEMOTION and MOUSE_POINT_ID in points
    ):
        points[MOUSE_POINT_ID] = _to_internal(*event.pos, window_size, normalized=False)
    elif event.type == pygame.MOUSEBUTTONUP:
        points.pop(MOUSE_POINT_ID, None)


def _present(window: pygame.Surface, internal: pygame.Surface) -> None:
    """内部描画面を縦横比を保って拡大し、ウィンドウの中央に表示する。"""
    window_size = window.get_size()
    window.fill(BLACK)
    view_w, view_h = _view_size(window_size)
    if view_w <= 0 or view_h <= 0:
        pygame.display.flip()
        return
    scaled = pygame.transform.scale(internal, (view_w, view_h))
    window.blit(
        scaled,
        (
            (window_size[0] - scaled.get_width()) // 2,
            (window_size[1] - scaled.get_height()) // 2,
        ),
    )
    pygame.display.flip()


async def main() -> None:
    pygame.init()
    pygame.display.set_caption("Mario-like")
    window = pygame.display.set_mode(
        (int(SCREEN_W * INITIAL_WINDOW_SCALE), int(SCREEN_H * INITIAL_WINDOW_SCALE)),
        pygame.RESIZABLE,
    )
    internal = pygame.Surface((SCREEN_W, SCREEN_H))
    assets = load_assets(IMAGE_DIR)
    session = GameSession(parse_stage(STAGE_PATH.read_text(encoding="utf-8")))
    touch_visible = detect_touch_device()
    layout = default_layout()
    clock = pygame.time.Clock()
    points: Points = {}
    accumulator = 0.0
    prev_jump_held = False

    while True:
        elapsed = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            _update_points(event, points, window.get_size())

        held = merge_held(
            keys_to_held(pygame.key.get_pressed()),
            points_to_held(list(points.values()), layout),
        )
        inp = make_input(held, prev_jump_held)
        accumulator = min(accumulator + elapsed, MAX_STEPS_PER_FRAME * FIXED_DT)
        steps = 0
        while accumulator >= FIXED_DT and steps < MAX_STEPS_PER_FRAME:
            session.update(inp, FIXED_DT)
            inp = replace(inp, jump_pressed=False)  # ジャンプ押下は最初のステップだけ
            accumulator -= FIXED_DT
            steps += 1
        if steps > 0:
            prev_jump_held = (
                held.jump
            )  # ステップが走らなかった描画フレームでは押下を持ち越す

        draw(internal, session, assets, touch_visible)
        _present(window, internal)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
