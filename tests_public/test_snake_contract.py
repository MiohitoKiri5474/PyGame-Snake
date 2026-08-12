from __future__ import annotations

from snake_trio.logic import advance_body, ate_food, hit_wall, next_head


def test_public_interfaces_are_importable() -> None:
    assert all(callable(item) for item in (next_head, ate_food, hit_wall, advance_body))


def test_next_head_moves_exactly_one_cell() -> None:
    assert next_head((40, 60), (1, 0), 20) == (60, 60)
    assert next_head((40, 60), (0, -1), 20) == (40, 40)


def test_ate_food_uses_exact_cell_equality() -> None:
    assert ate_food((20, 20), (20, 20)) is True
    assert ate_food((20, 20), (40, 20)) is False


def test_hit_wall_checks_all_four_edges() -> None:
    assert hit_wall((0, 0), 640, 480, 20) is False
    assert hit_wall((620, 460), 640, 480, 20) is False
    assert hit_wall((-20, 0), 640, 480, 20) is True
    assert hit_wall((640, 0), 640, 480, 20) is True
    assert hit_wall((0, -20), 640, 480, 20) is True
    assert hit_wall((0, 480), 640, 480, 20) is True


def test_advance_body_returns_a_new_list_and_obeys_growth() -> None:
    original = [(40, 20), (20, 20), (0, 20)]
    moved = advance_body(original, (60, 20), grow=False)
    grown = advance_body(original, (60, 20), grow=True)
    assert moved == [(60, 20), (40, 20), (20, 20)]
    assert grown == [(60, 20), (40, 20), (20, 20), (0, 20)]
    assert original == [(40, 20), (20, 20), (0, 20)]
    assert moved is not original and grown is not original
