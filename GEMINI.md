# GEMINI.md - Project Context

## Project Overview
**Snake Gemini** is a retro-style Nokia Snake game built as a teaching aid to demonstrate clean architecture, modern Python tooling, and decoupled logic. It mimics the "green-scale" aesthetic of the Nokia 3310 and GameBoy.

### Core Technologies
- **Language**: Python 3.11+
- **Game Engine**: `pygame` (ADR 1)
- **Tooling**: `uv` (ADR 4) for dependency management and project isolation.
- **Computer Vision**: `mediapipe` and `opencv-python` for optional hand-gesture control.
- **Architecture**: Decoupled `Snake` logic (independent of rendering) to allow for unit testing without a display environment.

## Architecture & Decisions
- **Snake Body**: Managed via `collections.deque` for $O(1)$ updates (ADR 2).
- **Game Loop**: Fixed-rate update loop using `pygame.time.Clock` to maintain the discrete "stepped" retro feel (ADR 3).
- **CV Controller**: `src/cv_controller.py` uses hand landmarker detection to map wrist/MCP tilt to direction changes.

## Building and Running

### Setup
Ensure [uv](https://github.com/astral-sh/uv) is installed.
```bash
uv sync
```

### Running the Game
- **Standard (Keyboard)**:
  ```bash
  uv run src/main.py
  ```
- **Gesture Control (Camera)**:
  ```bash
  uv run src/main.py --cv
  ```

### Testing
Tests use `unittest` and mock `pygame` to verify game rules programmatically.
```bash
uv run tests/test_snake.py
```

## Development Conventions
- **Code Style**: Functional separation between game logic (`Snake` class) and rendering (`Game` class).
- **Decision Records**: Major architectural changes should be documented in `docs/ADR.md`.
- **Coordinate System**: Grid-based (20x20 cells by default). Coordinates are `(x, y)` tuples.
- **Direction Lock**: Prevents 180-degree turns (e.g., cannot go LEFT if moving RIGHT).

## Key Files
- `src/main.py`: Entry point and core game/rendering logic.
- `src/cv_controller.py`: Logic for hand-gesture detection.
- `docs/SPECS.md`: Visual and mechanical requirements.
- `docs/ADR.md`: Rationales for library and data structure choices.
- `tests/test_snake.py`: Logic verification (wall collisions, growth, movement).
