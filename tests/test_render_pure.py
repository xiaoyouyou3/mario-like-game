"""DES-014〜016 render の純粋部分のテスト（pygame のウィンドウは作らない）。"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations

import pygame
import pytest

from src.game.geometry import Aabb
from src.game.input_state import HeldButtons
from src.game.stage_data import parse_stage
from src.game.tilemap import TileMap
from src.render.input_mapper import detect_touch_device, keys_to_held
from src.render.renderer import column_has_ground, compute_scale
from src.render.touch_controls import TouchLayout, default_layout, points_to_held
from tests.conftest import stage_text

BUTTONS = ("left", "right", "jump", "run")


def _only(name: str | None) -> HeldButtons:
    return HeldButtons(**{button: button == name for button in BUTTONS})


def _center(box: Aabb) -> tuple[float, float]:
    return (box.center_x, box.y + box.h / 2)


# TC-106
@pytest.mark.parametrize("name", BUTTONS)
def test_default_layout_button_fits_inside_the_internal_resolution(name: str) -> None:
    box = getattr(default_layout(), name)

    inside = (box.left >= 0, box.right <= 592, box.top >= 0, box.bottom <= 304)

    assert inside == (True, True, True, True)


# TC-123
@pytest.mark.parametrize("name", BUTTONS)
def test_default_layout_button_is_inside_the_control_panel(name: str) -> None:
    box = getattr(default_layout(), name)

    in_panel = (box.top >= 240, box.bottom <= 304)

    assert in_panel == (True, True)


# TC-124
@pytest.mark.parametrize(("first", "second"), list(combinations(BUTTONS, 2)))
def test_default_layout_buttons_do_not_overlap_each_other(first: str, second: str) -> None:
    layout = default_layout()

    overlap = getattr(layout, first).overlaps(getattr(layout, second))

    assert overlap is False


# TC-125
@pytest.mark.parametrize("name", BUTTONS)
def test_default_layout_button_is_at_least_48_px_wide_and_tall(name: str) -> None:
    box = getattr(default_layout(), name)

    size_ok = (box.w >= 48, box.h >= 48)

    assert size_ok == (True, True)


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
    [
        (592, 304, 1.0),
        (1184, 608, 2.0),
        (888, 456, 1.5),
        (1184, 304, 1.0),
        (592, 608, 1.0),
        (812, 375, 375 / 304),
    ],
)
def test_compute_scale_is_the_smaller_of_the_width_and_height_ratios(
    width: int, height: int, expected: float
) -> None:
    assert compute_scale(width, height) == pytest.approx(expected)


# TC-127
@pytest.mark.parametrize(("width", "height"), [(0, 304), (592, 0), (0, 0)])
def test_compute_scale_is_zero_for_a_window_with_no_width_or_height(width: int, height: int) -> None:
    assert compute_scale(width, height) == pytest.approx(0.0)


# TC-129
@pytest.mark.parametrize(("col", "expected"), [(9, True), (10, False), (11, False), (12, True)])
def test_column_has_ground_is_false_only_for_the_pit_columns(col: int, expected: bool) -> None:
    cells = {(10, 14): ".", (11, 14): "."}
    tilemap = TileMap(parse_stage(stage_text(cells, ground=True)))

    result = column_has_ground(tilemap, col)

    assert result is expected


# TC-130
def test_column_has_ground_looks_only_at_the_bottom_row() -> None:
    tilemap = TileMap(parse_stage(stage_text({(20, 13): "#"})))

    result = column_has_ground(tilemap, 20)

    assert result is False


# TC-131
@pytest.mark.parametrize("col", [-1, 200])
def test_column_has_ground_is_true_outside_the_stage_edges(col: int) -> None:
    tilemap = TileMap(parse_stage(stage_text()))

    result = column_has_ground(tilemap, col)

    assert result is True
