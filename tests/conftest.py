"""テスト共通の補助関数（docs/test-specs/test-spec.md §0）。"""

from __future__ import annotations

from collections.abc import Mapping

STAGE_W = 200
STAGE_H = 15
DEFAULT_START = (2, 13)
DEFAULT_FLAG = ((198, 12),)


def stage_text(
    cells: Mapping[tuple[int, int], str] | None = None,
    *,
    start: tuple[int, int] | None = DEFAULT_START,
    flag: tuple[tuple[int, int], ...] | None = DEFAULT_FLAG,
    ground: bool = False,
) -> str:
    """200x15 の全マスが '.' の文字列から、指定したマスだけ置き換えて作る。

    cells は {(col, row): 文字}。cells に 'P' / 'F' があれば、その指定を使い既定は置かない。
    start=None / flag=None で置かない。ground=True で row 14 を全部 '#' にする。
    """
    grid = [["."] * STAGE_W for _ in range(STAGE_H)]
    if ground:
        grid[14] = ["#"] * STAGE_W
    placed = dict(cells or {})
    values = set(placed.values())
    if start is not None and "P" not in values:
        placed[start] = "P"
    if flag is not None and "F" not in values:
        for col, row in flag:
            placed[(col, row)] = "F"
    for (col, row), ch in placed.items():
        grid[row][col] = ch
    return "\n".join("".join(row) for row in grid)
