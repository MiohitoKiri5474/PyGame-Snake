"""Add at least three trio-designed tests.

Write the expected result before running each test. Good targets include a
different direction, an exact board edge, growth by one segment, and proof that
the original body list is unchanged.
"""

from snake_trio.logic import ate_food, hit_wall, next_head

# def test_replace_with_a_meaningful_name() -> None:
#     # Arrange: create the smallest state that proves one contract rule.
#     # Act: call exactly one public function.
#     # Assert: compare an observable result with your written expectation.
#     raise NotImplementedError("Replace this scaffold with the trio's first test")


def test_range_of_head_positions() -> None:
    # Arrange: create the smallest state that proves one contract rule.
    # Act: call exactly one public function.
    # Assert: compare an observable result with your written expectation.

    assert next_head((60, 60), (1, 0), 20) == (80, 60)
    assert next_head((60, 60), (-1, 0), 20) == (40, 60)
    assert next_head((60, 60), (0, 1), 20) == (60, 80)
    assert next_head((60, 60), (0, -1), 20) == (60, 40)


def test_ate_food() -> None:
    assert ate_food((20, 40), (20, 40)) is True
    assert ate_food((60, 20), (20, 20)) is False


def test_hit_wall() -> None:
    assert hit_wall((0, 0), 640, 480, 20, 0) is False
    assert hit_wall((100, 100), 640, 480, 20, 0) is False
    assert hit_wall((620, 0), 640, 480, 20, 0) is False
    assert hit_wall((0, 460), 640, 480, 20, 0) is False

    assert hit_wall((640, 100), 640, 480, 20, 0) is True
    assert hit_wall((100, 480), 640, 480, 20, 0) is True
    assert hit_wall((-20, 100), 640, 480, 20, 0) is True
    assert hit_wall((100, -20), 640, 480, 20, 0) is True
