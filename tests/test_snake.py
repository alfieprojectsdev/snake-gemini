import unittest
from unittest.mock import MagicMock
import sys
import os

# Add src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Mock pygame before importing Snake from main
sys.modules['pygame'] = MagicMock()
from main import Snake, UP, DOWN, LEFT, RIGHT, GRID_SIZE

class TestSnake(unittest.TestCase):
    def setUp(self):
        self.snake = Snake()

    def test_initial_state(self):
        self.assertEqual(len(self.snake.body), 3)
        self.assertEqual(self.snake.direction, RIGHT)
        self.assertEqual(self.snake.body[0], (10, 10))

    def test_movement(self):
        self.snake.update()
        self.assertEqual(self.snake.body[0], (11, 10))
        self.assertEqual(len(self.snake.body), 3)

    def test_change_direction(self):
        self.snake.change_direction(UP)
        self.snake.update()
        self.assertEqual(self.snake.body[0], (10, 9))

    def test_prevent_180_turn(self):
        self.snake.change_direction(LEFT) # Current is RIGHT
        self.assertEqual(self.snake.new_direction, RIGHT)

    def test_growth(self):
        self.snake.grow = True
        self.snake.update()
        self.assertEqual(len(self.snake.body), 4)

    def test_collision_wall(self):
        # Move snake to the wall
        self.snake.body[0] = (GRID_SIZE - 1, 10)
        self.snake.update()
        self.assertTrue(self.snake.check_collision())

    def test_collision_self(self):
        # Manually create a self-collision scenario
        self.snake.body = [(10, 10), (11, 10), (11, 11), (10, 11), (10, 10)]
        self.assertTrue(self.snake.check_collision())

if __name__ == '__main__':
    unittest.main()
