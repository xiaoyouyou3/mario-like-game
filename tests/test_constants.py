"""DES-001 constants のテスト（要件から直接決まる値だけ）。"""

from __future__ import annotations

import pytest

from src.game import constants


# TC-112
def test_fixed_dt_is_one_sixtieth_of_a_second() -> None:
    dt = constants.FIXED_DT

    assert dt == pytest.approx(1 / 60)


# TC-113
def test_internal_resolution_is_592_by_304() -> None:
    size = (constants.SCREEN_W, constants.SCREEN_H)

    assert size == (592, 304)


# TC-126
def test_stage_area_is_240_px_and_control_panel_is_64_px() -> None:
    heights = (constants.PLAY_H, constants.PANEL_H)

    assert heights == (240, 64)


# TC-128
def test_touch_button_size_is_48_px() -> None:
    assert constants.TOUCH_BUTTON_SIZE == 48
