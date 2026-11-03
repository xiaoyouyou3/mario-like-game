"""DES-010 camera のテスト。"""

from __future__ import annotations

import pytest

from src.game.camera import next_camera_x

LEVEL_W = 3200


# TC-078
@pytest.mark.parametrize(
    ("center", "expected"),
    [(100, 0), (127, 0), (128, 0), (129, 1), (200, 72)],
)
def test_camera_follows_once_the_player_passes_the_screen_center(center: float, expected: float) -> None:
    result = next_camera_x(0, center, LEVEL_W)

    assert result == pytest.approx(expected)


# TC-079
def test_camera_never_moves_back_to_the_left() -> None:
    result = next_camera_x(500, 300, LEVEL_W)

    assert result == pytest.approx(500)


# TC-080
@pytest.mark.parametrize(
    ("prev", "center", "expected"),
    [(0, 3190, 2944), (2944, 100, 2944), (0, 0, 0)],
)
def test_camera_stays_within_the_stage(prev: float, center: float, expected: float) -> None:
    result = next_camera_x(prev, center, LEVEL_W)

    assert result == pytest.approx(expected)


# TC-116
@pytest.mark.parametrize(
    ("center", "expected"),
    [(700, 572), (3071, 2943), (3072, 2944), (3500, 2944)],
)
def test_camera_advances_from_a_nonzero_position_up_to_the_maximum(
    center: float, expected: float
) -> None:
    result = next_camera_x(500, center, LEVEL_W)

    assert result == pytest.approx(expected)
