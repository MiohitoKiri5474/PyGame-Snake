"""Supplied Pygame presentation shell for the Snake trio mission.

Students do not need to understand or edit this file during the core mission.
It translates keys, draws the board, and calls the four functions in logic.py.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

from .logic import (
    Cell,
    Direction,
    advance_body,
    ate_food,
    hit_wall,
    next_head,
    shrink_body,
)

WIDTH = 640
HEIGHT = 480
CELL = 20
START_BODY: list[Cell] = [(200, 200), (180, 200), (160, 200)]
START_DIRECTION: Direction = (1, 0)
HEADER_HEIGHT = 40
SPEED = [1, 1.2, 1.3, 1.4, 1.5]
LEVEL_BACKGROUNDS = [
    (255, 253, 249),  # Level 1: Original
    (170, 215, 255),  # Level 2: Ocean
    (180, 225, 170),  # Level 3: Jungle
    (245, 220, 150),  # Level 4: Pyramid
    (255, 200, 225),  # Level 5: Princess
]


def choose_food(body: list[Cell]) -> Cell:
    """Choose the first free cell deterministically for reproducible play."""
    if len(body) >= (WIDTH // CELL) * (HEIGHT // CELL):
        raise RuntimeError("board is full")

    x = random.randint(0, WIDTH // CELL - 1) * CELL
    y = random.randint(HEADER_HEIGHT, (HEIGHT + HEADER_HEIGHT) // CELL - 1) * CELL
    while (x, y) in body:
        x = random.randint(0, WIDTH // CELL - 1) * CELL
        y = random.randint(HEADER_HEIGHT, (HEIGHT + HEADER_HEIGHT) // CELL - 1) * CELL
    return (x, y)


@dataclass
class GameState:
    body: list[Cell]
    direction: Direction
    food: Cell
    score: int = 0
    level: int = 1
    game_over: bool = False
    bad_food: Cell | None = None
    bad_food_expire_time: int = 0


def new_game() -> GameState:
    body = list(START_BODY)
    return GameState(body=body, direction=START_DIRECTION, food=choose_food(body))


def step(state: GameState) -> None:
    # 1. 算出新的頭部位置
    new_head = next_head(state.body[0], state.direction, CELL)

    # 2. 檢查是否吃到「正常食物」
    grow = ate_food(new_head, state.food)

    # --- 【新增區塊開始】 ---
    # 3. 檢查是否吃到「毒蘋果」
    ate_bad = False
    # 確認畫面上目前有毒蘋果，且蛇頭碰到了它
    if state.bad_food is not None and ate_food(new_head, state.bad_food):
        ate_bad = True
        state.score = max(0, state.score - 1)  # 扣 1 分 (用 max 確保不會扣到負分)
        state.bad_food = None  # 吃掉後毒蘋果就消失

    # 4. 決定下一個身體的狀態
    if ate_bad:
        # 如果吃到毒蘋果，呼叫縮短邏輯
        next_body = shrink_body(state.body, new_head)
    else:
        # 否則，按照原本的邏輯正常移動或長大
        next_body = advance_body(state.body, new_head, grow)
    # --- 【新增區塊結束】 ---

    # 5. 檢查碰撞 (撞牆或撞到自己)
    self_hit = new_head in next_body[1:]
    if hit_wall(new_head, WIDTH, HEIGHT, CELL, HEADER_HEIGHT) or self_hit:
        state.game_over = True
        return

    # 6. 正式更新蛇身
    state.body = next_body

    # 7. 如果吃到正常食物，加分並產生新食物
    if grow:
        state.score += 1
        state.food = choose_food(state.body)

    if state.score % 10 == 0 and state.score != 0:
        state.level = min(state.level + 1, len(SPEED))


def run_game() -> int:
    try:
        import pygame
    except ImportError:
        print("Pygame is not installed. Run: python -m pip install -e '.[display]' ")
        return 2

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + HEADER_HEIGHT))
    pygame.display.set_caption("NCKU Snake Trio Studio")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    state = new_game()
    next_step = pygame.time.get_ticks() + 130 / SPEED[state.level - 1]
    running = True

    key_directions = {
        pygame.K_LEFT: (-1, 0),
        pygame.K_a: (-1, 0),
        pygame.K_RIGHT: (1, 0),
        pygame.K_d: (1, 0),
        pygame.K_UP: (0, -1),
        pygame.K_w: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_s: (0, 1),
    }

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state = new_game()
                    next_step = pygame.time.get_ticks() + 130 / SPEED[state.level - 1]
                elif event.key in key_directions and not state.game_over:
                    candidate = key_directions[event.key]
                    if candidate != (-state.direction[0], -state.direction[1]):
                        state.direction = candidate

        now = pygame.time.get_ticks()
        # 【新增】毒蘋果生成與消失邏輯
        if not state.game_over:
            # 如果畫面上沒有毒蘋果，有小機率生成 (或者使用固定計時器)
            if state.bad_food is None:
                import random

                # 這裡設定一個機率，每偵測一次有很小的機率生成
                if random.random() < 0.005:
                    try:
                        state.bad_food = choose_food(state.body + [state.food])
                        state.bad_food_expire_time = (
                            now + 20000
                        )  # 20秒 (20000毫秒) 後消失
                    except RuntimeError:
                        pass  # 版面滿了就不生成
            else:
                # 檢查毒蘋果是否過期
                if now >= state.bad_food_expire_time:
                    state.bad_food = None
        if not state.game_over and now >= next_step:
            step(state)
            next_step += 130 / SPEED[state.level - 1]

        background_color = LEVEL_BACKGROUNDS[state.level - 1]
        screen.fill(background_color)

        # --- Header block: score + level ---
        pygame.draw.rect(screen, (235, 230, 221), (0, 0, WIDTH, HEADER_HEIGHT))
        pygame.draw.line(
            screen, (226, 218, 207), (0, HEADER_HEIGHT), (WIDTH, HEADER_HEIGHT)
        )
        header_text = f"Score {state.score} | Level {state.level}"
        screen.blit(font.render(header_text, True, (66, 10, 21)), (12, 8))

        # --- Game field (shifted down by HEADER_HEIGHT) ---
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(
                screen, (226, 218, 207), (x, HEADER_HEIGHT), (x, HEADER_HEIGHT + HEIGHT)
            )
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(
                screen,
                (226, 218, 207),
                (0, HEADER_HEIGHT + y),
                (WIDTH, HEADER_HEIGHT + y),
            )
        for index, (x, y) in enumerate(state.body):
            color = (39, 118, 91) if index == 0 else (94, 153, 93)
            pygame.draw.rect(
                screen, color, (x + 1, y + 1, CELL - 2, CELL - 2), border_radius=5
            )
        fx, fy = state.food
        pygame.draw.circle(
            screen, (220, 92, 72), (fx + CELL // 2, fy + CELL // 2), CELL // 2 - 2
        )

        if state.game_over:
            over_text = "Game over - press R to restart"
            screen.blit(
                font.render(over_text, True, (66, 10, 21)),
                (12, HEADER_HEIGHT + 10),
            )
        if state.bad_food:
            bx, by = state.bad_food
            pygame.draw.circle(
                screen, (138, 43, 226), (bx + CELL // 2, by + CELL // 2), CELL // 2 - 2
            )
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true", help="run one deterministic logic step"
    )
    args = parser.parse_args(argv)
    if args.check:
        state = new_game()
        step(state)
        print({"head": state.body[0], "length": len(state.body), "score": state.score})
        return 0
    return run_game()
