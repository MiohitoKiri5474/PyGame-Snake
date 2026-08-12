"""Supplied Pygame presentation shell for the Snake trio mission.

Students do not need to understand or edit this file during the core mission.
It translates keys, draws the board, and calls the four functions in logic.py.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from .logic import Cell, Direction, advance_body, ate_food, hit_wall, next_head

WIDTH = 640
HEIGHT = 480
CELL = 20
STEP_MS = 130
START_BODY: list[Cell] = [(200, 200), (180, 200), (160, 200)]
START_DIRECTION: Direction = (1, 0)


def choose_food(body: list[Cell]) -> Cell:
    """Choose the first free cell deterministically for reproducible play."""
    for y in range(0, HEIGHT, CELL):
        for x in range(0, WIDTH, CELL):
            if (x, y) not in body:
                return (x, y)
    raise RuntimeError("board is full")


@dataclass
class GameState:
    body: list[Cell]
    direction: Direction
    food: Cell
    score: int = 0
    game_over: bool = False


def new_game() -> GameState:
    body = list(START_BODY)
    return GameState(body=body, direction=START_DIRECTION, food=choose_food(body))


def step(state: GameState) -> None:
    new_head = next_head(state.body[0], state.direction, CELL)
    grow = ate_food(new_head, state.food)
    next_body = advance_body(state.body, new_head, grow)
    self_hit = new_head in next_body[1:]
    if hit_wall(new_head, WIDTH, HEIGHT, CELL) or self_hit:
        state.game_over = True
        return
    state.body = next_body
    if grow:
        state.score += 1
        state.food = choose_food(state.body)


def run_game() -> int:
    try:
        import pygame
    except ImportError:
        print("Pygame is not installed. Run: python -m pip install -e '.[display]' ")
        return 2

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("NCKU Snake Trio Studio")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    state = new_game()
    next_step = pygame.time.get_ticks() + STEP_MS
    running = True

    key_directions = {
        pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
        pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
        pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
        pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
    }

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state = new_game()
                    next_step = pygame.time.get_ticks() + STEP_MS
                elif event.key in key_directions and not state.game_over:
                    candidate = key_directions[event.key]
                    if candidate != (-state.direction[0], -state.direction[1]):
                        state.direction = candidate

        now = pygame.time.get_ticks()
        if not state.game_over and now >= next_step:
            step(state)
            next_step += STEP_MS

        screen.fill((255, 253, 249))
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, (226, 218, 207), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(screen, (226, 218, 207), (0, y), (WIDTH, y))
        for index, (x, y) in enumerate(state.body):
            color = (39, 118, 91) if index == 0 else (94, 153, 93)
            pygame.draw.rect(screen, color, (x + 1, y + 1, CELL - 2, CELL - 2), border_radius=5)
        fx, fy = state.food
        pygame.draw.circle(screen, (220, 92, 72), (fx + CELL // 2, fy + CELL // 2), CELL // 2 - 2)
        message = f"Score {state.score}"
        if state.game_over:
            message += "  |  Game over - press R to restart"
        screen.blit(font.render(message, True, (66, 10, 21)), (12, 10))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run one deterministic logic step")
    args = parser.parse_args(argv)
    if args.check:
        state = new_game()
        step(state)
        print({"head": state.body[0], "length": len(state.body), "score": state.score})
        return 0
    return run_game()
