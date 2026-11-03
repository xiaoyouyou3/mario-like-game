"""DES-006 physics のテスト。"""

from __future__ import annotations

import pytest

from src.game.geometry import Aabb
from src.game.physics import Body, CollisionResult, apply_gravity, move_and_collide
from src.game.stage_data import parse_stage
from src.game.tilemap import TileMap
from tests.conftest import stage_text

DT = 1 / 60
NO_HIT = CollisionResult(False, False, False, None)


def _map(cells: dict[tuple[int, int], str] | None = None, *, ground: bool = False) -> TileMap:
    return TileMap(parse_stage(stage_text(cells, ground=ground)))


def _body(
    x: float, y: float, *, vx: float = 0.0, vy: float = 0.0, on_ground: bool = False
) -> Body:
    return Body(Aabb(x, y, 12, 16), vx=vx, vy=vy, on_ground=on_ground)


# TC-022
@pytest.mark.parametrize(("vy", "expected"), [(0, 15), (-345, -330), (100, 115)])
def test_apply_gravity_adds_gravity_times_dt_to_vy(vy: float, expected: float) -> None:
    body = _body(0, 0, vy=vy)

    apply_gravity(body, DT)

    assert body.vy == pytest.approx(expected)


# TC-023
@pytest.mark.parametrize(("vy", "expected"), [(224, 239), (225, 240), (240, 240)])
def test_apply_gravity_caps_vy_at_240(vy: float, expected: float) -> None:
    body = _body(0, 0, vy=vy)

    apply_gravity(body, DT)

    assert body.vy == pytest.approx(expected)


# TC-024
def test_move_and_collide_moves_a_body_through_empty_space() -> None:
    body = _body(100, 100, vx=60)

    result = move_and_collide(body, _map(), DT)

    state = (body.box.x, body.box.y, body.on_ground, result, body.vx)
    assert state == (pytest.approx(101), pytest.approx(100), False, NO_HIT, 60)


# TC-025
def test_move_and_collide_does_not_move_a_body_when_dt_is_zero() -> None:
    body = _body(100, 100, vx=60, vy=120)

    move_and_collide(body, _map(), 0.0)

    assert (body.box.x, body.box.y) == (pytest.approx(100), pytest.approx(100))


# TC-026
def test_move_and_collide_lands_a_falling_body_on_the_floor() -> None:
    body = _body(100, 207, vy=120)

    move_and_collide(body, _map(ground=True), DT)

    assert (body.box.y, body.vy, body.on_ground) == (pytest.approx(208), 0, True)


# TC-027
def test_move_and_collide_keeps_a_standing_body_on_the_floor() -> None:
    body = _body(100, 208, vy=15, on_ground=True)

    move_and_collide(body, _map(ground=True), DT)

    assert (body.box.y, body.vy, body.on_ground) == (pytest.approx(208), 0, True)


# TC-028
def test_move_and_collide_leaves_the_ground_when_the_floor_ends() -> None:
    floor = {(col, 14): "#" for col in range(6)}
    body = _body(100, 208, vy=15, on_ground=True)

    move_and_collide(body, _map(floor), DT)

    state = (body.box.y, body.vy, body.on_ground)
    assert state == (pytest.approx(208.25), pytest.approx(15), False)


# TC-029
@pytest.mark.parametrize(
    ("x", "vx", "hit_right"),
    [(147, 120, True), (148, 0, False), (148, 60, True)],
)
def test_move_and_collide_stops_a_body_at_the_left_face_of_a_wall(
    x: float, vx: float, hit_right: bool
) -> None:
    wall = {(10, 12): "#", (10, 13): "#"}
    body = _body(x, 200, vx=vx)

    result = move_and_collide(body, _map(wall), DT)

    assert (body.box.x, body.vx, result.hit_right) == (pytest.approx(148), 0, hit_right)


# TC-030
def test_move_and_collide_stops_a_body_at_the_right_face_of_a_wall() -> None:
    wall = {(5, 12): "#", (5, 13): "#"}
    body = _body(96.5, 200, vx=-60)

    result = move_and_collide(body, _map(wall), DT)

    assert (body.box.x, body.vx, result.hit_left) == (pytest.approx(96), 0, True)


# TC-031
@pytest.mark.parametrize(
    ("x", "expected"),
    [
        (98, (144, 0, True, (6, 8))),
        (112, (143.5, -60, False, None)),
    ],
)
def test_move_and_collide_stops_a_rising_body_at_a_ceiling_tile(
    x: float, expected: tuple[float, float, bool, tuple[int, int] | None]
) -> None:
    body = _body(x, 144.5, vy=-60)

    result = move_and_collide(body, _map({(6, 8): "#"}), DT)

    actual = (body.box.y, body.vy, result.hit_ceiling, result.ceiling_cell)
    assert actual == (pytest.approx(expected[0]), expected[1], expected[2], expected[3])


# TC-032
@pytest.mark.parametrize(("x", "cell"), [(89, (5, 8)), (90, (5, 8)), (91, (6, 8))])
def test_move_and_collide_reports_the_ceiling_tile_nearest_to_the_body_center(
    x: float, cell: tuple[int, int]
) -> None:
    body = _body(x, 144.5, vy=-60)

    result = move_and_collide(body, _map({(5, 8): "#", (6, 8): "#"}), DT)

    assert result.ceiling_cell == cell


# TC-033
def test_move_and_collide_resolves_x_before_y_at_a_wall_base_corner() -> None:
    cells = {(10, 12): "#", (10, 13): "#"}
    body = _body(147, 207, vx=120, vy=120)

    result = move_and_collide(body, _map(cells, ground=True), DT)

    state = (body.box.x, body.box.y, body.vx, body.vy, body.on_ground, result.hit_right)
    assert state == (pytest.approx(148), pytest.approx(208), 0, 0, True, True)


# TC-034
@pytest.mark.parametrize(
    ("x", "vx", "expected_x", "side"),
    [(0.5, -60, 0, "hit_left"), (3187.5, 60, 3188, "hit_right")],
)
def test_move_and_collide_treats_the_stage_edges_as_walls(
    x: float, vx: float, expected_x: float, side: str
) -> None:
    body = _body(x, 200, vx=vx)

    result = move_and_collide(body, _map(), DT)

    assert (body.box.x, body.vx, getattr(result, side)) == (pytest.approx(expected_x), 0, True)


# TC-035
def test_falling_speed_reaches_240_and_never_exceeds_it() -> None:
    body = _body(100, 0)
    tilemap = _map()

    speeds = []
    for _ in range(100):
        apply_gravity(body, DT)
        move_and_collide(body, tilemap, DT)
        speeds.append(body.vy)

    assert max(speeds) == pytest.approx(240)
