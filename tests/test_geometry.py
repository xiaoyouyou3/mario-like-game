"""DES-003 geometry のテスト。"""

from __future__ import annotations

import pytest

from src.game.geometry import Aabb, tile_span


# TC-004
def test_aabb_exposes_edges_and_center() -> None:
    box = Aabb(10, 20, 30, 40)

    edges = (box.left, box.right, box.top, box.bottom, box.center_x)

    assert edges == (10, 40, 20, 60, 25)


# TC-005
@pytest.mark.parametrize(
    ("other", "expected"),
    [
        (Aabb(8, 8, 16, 16), True),
        (Aabb(15, 0, 16, 16), True),
        (Aabb(16, 0, 16, 16), False),
        (Aabb(0, 16, 16, 16), False),
        (Aabb(40, 40, 16, 16), False),
    ],
)
def test_aabb_overlaps_is_false_when_boxes_only_touch_at_an_edge(other: Aabb, expected: bool) -> None:
    box = Aabb(0, 0, 16, 16)

    result = box.overlaps(other)

    assert result is expected


# TC-006
@pytest.mark.parametrize(
    ("lo", "hi", "expected"),
    [
        (0, 16, [0]),
        (0, 16.5, [0, 1]),
        (16, 32, [1]),
        (-1, 1, [-1, 0]),
        (15.9, 16.1, [0, 1]),
    ],
)
def test_tile_span_returns_tiles_overlapped_by_the_half_open_interval(
    lo: float, hi: float, expected: list[int]
) -> None:
    result = tile_span(lo, hi)

    assert list(result) == expected
