"""Four small, testable rules used by the supplied Pygame shell.

Your trio edits only this file for the core mission.  Keep every function pure:
do not import Pygame, open a window, read the keyboard, or change the supplied
``body`` list in place.
"""

from __future__ import annotations

Cell = tuple[int, int]
Direction = tuple[int, int]


def next_head(head: Cell, direction: Direction, cell_size: int) -> Cell:
    """Return the next head cell.

    Interface:
        head: current ``(x, y)`` grid position.
        direction: one of ``(-1, 0)``, ``(1, 0)``, ``(0, -1)``, ``(0, 1)``.
        cell_size: positive number of pixels moved in one step.
        return: a new ``(x, y)`` tuple.

    Hint: calculate x and y separately.  Do not mutate any input.
    """
    # TODO 1: replace this line with one return statement.
    raise NotImplementedError("TODO 1: compute the next head")


def ate_food(head: Cell, food: Cell) -> bool:
    """Return True exactly when the snake head occupies the food cell.

    Hint: both values use the same ``(x, y)`` tuple format.
    """
    # TODO 2: replace this line with one boolean return statement.
    raise NotImplementedError("TODO 2: compare head and food")


def hit_wall(head: Cell, width: int, height: int, cell_size: int) -> bool:
    """Return True when any part of the head is outside the board.

    Legal x values begin at 0 and stop before ``width``.
    Legal y values begin at 0 and stop before ``height``.
    The head is aligned to the grid, so its top-left coordinate is enough.
    """
    # TODO 3: check left, right, top, and bottom boundaries.
    raise NotImplementedError("TODO 3: check four wall boundaries")


def advance_body(body: list[Cell], new_head: Cell, grow: bool) -> list[Cell]:
    """Return the next snake body without changing ``body``.

    The returned list always begins with ``new_head``.  When ``grow`` is True,
    keep every old segment.  Otherwise remove only the old tail.
    """
    # TODO 4: build and return a new list.  Never call body.insert/pop/remove.
    raise NotImplementedError("TODO 4: create the next body")
