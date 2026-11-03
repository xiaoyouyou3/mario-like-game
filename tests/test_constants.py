"""DES-001 constants のテスト（要件から直接決まる値だけ）。"""

from __future__ import annotations

import pytest

from src.game import constants


# TC-112
def test_fixed_dt_is_one_sixtieth_of_a_second() -> None:
    dt = constants.FIXED_DT

    assert dt == pytest.approx(1 / 60)


# TC-113
def test_internal_resolution_is_256_by_240() -> None:
    size = (constants.SCREEN_W, constants.SCREEN_H)

    assert size == (256, 240)
