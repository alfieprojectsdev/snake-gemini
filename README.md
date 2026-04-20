# Nokia-Style Snake Game (Teaching Aid)

A retro-style Snake game built with Python and `pygame`, designed as a pedagogical example of clean architecture, modern Python tooling, and retro-game design.

## 🎓 Why this project?
This repository is designed to demonstrate several core software engineering principles:
1.  **Architecture Decision Records (ADRs)**: Documenting *why* decisions were made (e.g., why `deque` over `list`).
2.  **Decoupled Logic**: The `Snake` class is independent of `pygame`, allowing it to be unit-tested in environments without a GPU/Display.
3.  **Modern Tooling**: Leveraging `uv` for lightning-fast, reproducible dependency management.
4.  **Steelman Design**: Practicing the "Steelman" of tradeoffs—defending the strongest version of an alternative before rejecting it.
5.  **Multi-threaded CV Integration**: Integrating low-latency Computer Vision (Mediapipe) for gesture controls.

## 🛠 Features
- **Retro Aesthetic**: "Green-scale" color palette (`#9bbc0f`, `#0f380f`) and grid-based visuals mimicking the Nokia 3310.
- **Gesture Control (NEW)**: Use hand-tilt ("flick") gestures to control the snake. Built with Mediapipe and OpenCV.
- **Efficient Data Structures**: Uses `collections.deque` for $O(1)$ snake movement and `itertools.islice` for zero-copy collision detection.
- **Robust Multithreading**: Thread-safe move delivery using `queue.Queue` and `threading.Event` for reliable controller lifecycles.

## 🚀 Getting Started
Ensure you have [uv](https://github.com/astral-sh/uv) installed.

### 1. Setup
```bash
uv sync
```

### 2. Run the Game
- **Standard (Keyboard)**:
  ```bash
  uv run src/main.py
  ```
- **Gesture Control (Camera)**:
  ```bash
  uv run src/main.py --cv
  ```

### 3. Run Tests
Observe how tests run without opening a window, thanks to logic decoupling:
```bash
uv run tests/test_snake.py
```

## 📖 Learning Path
- **Step 1: The Specs**: Read `docs/SPECS.md` to understand the "What".
- **Step 2: The Decisions**: Read `docs/ADR.md` to understand the "Why".
- **Step 3: The Logic**: Explore `src/main.py` and see how the `Snake` class manages coordinates without knowing about colors or pixels.
- **Step 4: The CV Controller**: Check `src/cv_controller.py` to see how wrist tilt is mapped to game directions using relative vectors.
- **Step 5: The Validation**: Check `tests/test_snake.py` to see how we verify game rules programmatically.

## 🧪 Customization & Exercises
This project is built to be modified. Here are some exercises to help you understand the code:

### 1. Change Key Bindings
Open `src/main.py` and find the `handle_input` method.
- **Challenge**: Replace `WASD` with `IJKL` keys.

### 2. Adjust Game Speed
In `src/main.py`, find the `update` method.
- **Challenge**: Make the game speed up faster.

### 3. Change the Palette
Find the "Colors" section at the top of `src/main.py`.
- **Challenge**: Change the "Nokia Green" to a "Cyberpunk Pink/Neon" theme.

### 4. Fine-tune Gestures
In `src/cv_controller.py`, adjust the `0.1` deadzone threshold or the `throttle` time.
- **Challenge**: Make the gesture controls more or less sensitive.

## 🕹 Controls
- **WASD / Arrow Keys**: Move
- **Hand Tilt**: Move (when running with `--cv`)
- **R**: Restart (after Game Over)
- **Esc**: Quit

---
*For AI agents and developers: See [GEMINI.md](./GEMINI.md) for full architectural context.*
