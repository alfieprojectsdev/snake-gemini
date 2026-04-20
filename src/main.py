import pygame
import random
import sys
from collections import deque

# Constants from SPECS
WINDOW_SIZE = 400
GRID_SIZE = 20
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

# Colors (Nokia 3310 / GameBoy Green-scale)
COLOR_BG = (155, 188, 15)   # #9bbc0f (Light Green)
COLOR_SNAKE = (15, 56, 15)  # #0f380f (Dark Green)
COLOR_FOOD = (15, 56, 15)   # #0f380f (Dark Green)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

from itertools import islice

class Snake:
    def __init__(self):
        # Start at center (10, 10) with 3 segments
        self.body = deque([(10, 10), (9, 10), (8, 10)])
        self.direction = RIGHT
        self.new_direction = RIGHT
        self.grow = False

    def update(self):
        self.direction = self.new_direction
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        self.body.appendleft(new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_dir):
        # Prevent 180-degree turns
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.new_direction = new_dir

    def check_collision(self):
        head = self.body[0]
        # Wall collision
        if not (0 <= head[0] < GRID_SIZE and 0 <= head[1] < GRID_SIZE):
            return True
        # Self collision
        if head in islice(self.body, 1, None):
            return True
        return False

from cv_controller import SnakeGestureController

class Game:
    def __init__(self, use_cv=False):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Nokia Snake - Gemini")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 15)
        self.use_cv = use_cv
        self.cv_ctrl = SnakeGestureController() if use_cv else None
        self.reset()

    def reset(self):
        self.snake = Snake()
        self.food = self._spawn_food()
        self.score = 0
        self.fps = 10
        self.game_over = False
        if self.use_cv and self.cv_ctrl is not None:
            self.cv_ctrl.stop()
            self.cv_ctrl.start()

    def _spawn_food(self):
        while True:
            food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if food not in self.snake.body:
                return food

    def handle_input(self):
        if self.use_cv:
            move = self.cv_ctrl.get_move()
            if move == 'UP': self.snake.change_direction(UP)
            elif move == 'DOWN': self.snake.change_direction(DOWN)
            elif move == 'LEFT': self.snake.change_direction(LEFT)
            elif move == 'RIGHT': self.snake.change_direction(RIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.use_cv: self.cv_ctrl.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.snake.change_direction(UP)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.snake.change_direction(RIGHT)
                elif event.key == pygame.K_ESCAPE:
                    if self.use_cv: self.cv_ctrl.stop()
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r and self.game_over:
                    self.reset()

    def update(self):
        if self.game_over:
            return

        self.snake.update()

        if self.snake.check_collision():
            self.game_over = True
            return

        if self.snake.body[0] == self.food:
            self.snake.grow = True
            self.food = self._spawn_food()
            self.score += 10
            # Speed increases every 50 points (5 food items)
            if self.score % 50 == 0:
                self.fps += 1

    def draw(self):
        self.screen.fill(COLOR_BG)

        # Draw Food
        food_rect = pygame.Rect(self.food[0] * CELL_SIZE, self.food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, COLOR_FOOD, food_rect.inflate(-4, -4)) # Inset to look like a dot

        # Draw Snake
        for segment in self.snake.body:
            seg_rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, COLOR_SNAKE, seg_rect.inflate(-2, -2)) # Border effect

        # Draw Score
        score_text = self.font.render(f"SCORE: {self.score}", True, COLOR_SNAKE)
        self.screen.blit(score_text, (5, 5))

        if self.game_over:
            over_text = self.font.render("GAME OVER - PRESS R TO RESTART", True, COLOR_SNAKE)
            text_rect = over_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
            self.screen.blit(over_text, text_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--cv", action="store_true")
    args = parser.parse_args()
    game = Game(use_cv=args.cv)
    game.run()
