"""DES-002 input_state のテスト。"""

from __future__ import annotations

import pytest

from src.game.input_state import HeldButtons, make_input, merge_held


def held(*, left: bool = False, right: bool = False, jump: bool = False, run: bool = False) -> HeldButtons:
    return HeldButtons(left=left, right=right, jump=jump, run=run)


# TC-001
@pytest.mark.parametrize(
    ("jump", "prev", "expected"),
    [(True, False, True), (True, True, False), (False, True, False), (False, False, False)],
)
def test_make_input_sets_jump_pressed_only_on_the_frame_the_button_goes_down(
    jump: bool, prev: bool, expected: bool
) -> None:
    buttons = held(jump=jump)

    result = make_input(buttons, prev)

    assert result.jump_pressed is expected


# TC-002
@pytest.mark.parametrize("field", ["left", "right", "run"])
def test_make_input_copies_direction_and_run_from_held_buttons(field: str) -> None:
    buttons = held(**{field: True})

    result = make_input(buttons, False)

    assert getattr(result, field) is True
    assert [getattr(result, f) for f in ("left", "right", "run") if f != field] == [False, False]


# TC-003
def test_merge_held_combines_two_states_by_or_per_button() -> None:
    a = held(left=True)
    b = held(right=True, jump=True)

    merged = merge_held(a, b)

    assert merged == held(left=True, right=True, jump=True, run=False)
