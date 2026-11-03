"""入力状態の型と変換。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HeldButtons:
    left: bool
    right: bool
    jump: bool
    run: bool


@dataclass(frozen=True)
class InputState:
    left: bool
    right: bool
    run: bool
    jump_pressed: bool


def make_input(held: HeldButtons, prev_jump_held: bool) -> InputState:
    """jump_pressed は押した瞬間（今回押下・前回非押下）だけ真にする。"""
    return InputState(
        left=held.left,
        right=held.right,
        run=held.run,
        jump_pressed=held.jump and not prev_jump_held,
    )


def merge_held(a: HeldButtons, b: HeldButtons) -> HeldButtons:
    """項目ごとの OR。"""
    return HeldButtons(
        left=a.left or b.left,
        right=a.right or b.right,
        jump=a.jump or b.jump,
        run=a.run or b.run,
    )
