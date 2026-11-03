"""DES-014〜016 render の純粋部分のテスト（pygame のウィンドウは作らない）。"""

from __future__ import annotations

from collections import defaultdict

import pygame
import pytest

from src.game.geometry import Aabb
from src.game.input_state import HeldButtons
from src.render.input_mapper import detect_touch_device, keys_to_held
from src.render.renderer import compute_scale
from src.render.touch_controls import TouchLayout, default_layout, points_to_held

BUTTONS = ("left", "right", "jump", "run")


def _only(name: str | None) -> HeldButtons:
    return HeldButtons(**{button: button == name for button in BUTTONS})


def _center(box: Aabb) -> tuple[float, float]:
    return (box.center_x, box.y + box.h / 2)


# TC-106
def test_default_layout_fits_the_screen_without_overlapping_buttons() -> None:
    layout = default_layout()
    boxes = [layout.left, layout.right, layout.jump, layout.run]

    inside = all(0 <= b.left and b.right <= 256 and 0 <= b.top and b.bottom <= 240 for b in boxes)
    pairs_overlap = [
        boxes[i].overlaps(boxes[j]) for i in range(len(boxes)) for j in range(i + 1, len(boxes))
    ]
    assert (inside, any(pairs_overlap)) == (True, False)


# TC-107
@pytest.mark.parametrize("name", BUTTONS)
def test_pressing_the_center_of_a_button_presses_only_that_button(name: str) -> None:
    layout = default_layout()

    held = points_to_held([_center(getattr(layout, name))], layout)

    assert held == _only(name)


# TC-108
@pytest.mark.parametrize(
    ("points", "expected"),
    [
        ([(0, 100)], _only("left")),
        ([(40, 100)], _only(None)),
        ([(39.9, 139.9)], _only("left")),
        ([(20, 120), (220, 120)], HeldButtons(left=True, right=False, jump=True, run=False)),
        ([], _only(None)),
    ],
)
def test_button_edges_include_top_left_and_exclude_bottom_right(
    points: list[tuple[float, float]], expected: HeldButtons
) -> None:
    layout = TouchLayout(
        left=Aabb(0, 100, 40, 40),
        right=Aabb(50, 100, 40, 40),
        jump=Aabb(200, 100, 40, 40),
        run=Aabb(150, 100, 40, 40),
    )

    held = points_to_held(points, layout)

    assert held == expected


# TC-109
@pytest.mark.parametrize(
    ("key", "name"),
    [
        (pygame.K_LEFT, "left"),
        (pygame.K_RIGHT, "right"),
        (pygame.K_z, "jump"),
        (pygame.K_x, "run"),
        (pygame.K_a, None),
    ],
)
def test_keys_and_touch_produce_the_same_held_buttons(key: int, name: str | None) -> None:
    pressed: defaultdict[int, bool] = defaultdict(bool)
    pressed[key] = True
    layout = default_layout()
    touched = [] if name is None else [_center(getattr(layout, name))]

    from_keys = keys_to_held(pressed)

    assert from_keys == points_to_held(touched, layout) == _only(name)


# TC-110
def test_touch_device_is_not_detected_outside_the_browser() -> None:
    assert detect_touch_device() is False


# TC-111
@pytest.mark.parametrize(
    ("width", "height", "expected"),
    [(256, 240, 1), (512, 480, 2), (511, 480, 1), (1024, 720, 3), (255, 239, 1), (100, 100, 1), (800, 600, 2)],
)
def test_compute_scale_is_the_largest_whole_multiple_that_fits(
    width: int, height: int, expected: int
) -> None:
    assert compute_scale(width, height) == expected
