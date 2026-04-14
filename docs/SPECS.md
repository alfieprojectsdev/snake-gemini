# Game Specifications: Nokia Snake

## Visual Style
- **Color Palette**: Retro GameBoy / Nokia 3310 "green-scale".
  - Background: `#9bbc0f` (Light Green)
  - Snake/Food: `#0f380f` (Dark Green)
- **Resolution**: 400x400 pixels.
- **Grid Size**: 20x20 cells (Each cell is 20x20 pixels).

## Mechanics
- **Snake Movement**: The snake moves one grid cell per "tick".
- **Initial State**:
  - Snake starts at center with 3 segments.
  - Initial direction: RIGHT.
  - Initial speed: 10 ticks per second (10 FPS).
- **Growth**: Snake grows by one segment for each food eaten.
- **Food**: One food item appears at a random location not occupied by the snake.
- **Score**:
  - 10 points per food item.
  - Speed increases every 5 food items eaten.
- **Game Over Conditions**:
  - Snake hits a wall.
  - Snake hits itself.

## Controls
- **Arrow Keys** or **WASD**: Change direction (UP, DOWN, LEFT, RIGHT).
- **Escape**: Quit game.
- **Direction Lock**: The snake cannot move in the opposite direction of its current movement (e.g., cannot go DOWN if currently moving UP).

## Technical Requirements
- Python 3.x
- `pygame` library
