# Nokia-Style Snake Game (Teaching Aid)

A retro-style Snake game built with Python and `pygame`, designed as a pedagogical example of clean architecture, modern Python tooling, and retro-game design.

## 🎓 Why this project?
This repository is designed to demonstrate several core software engineering principles:
1.  **Architecture Decision Records (ADRs)**: Documenting *why* decisions were made (e.g., why `deque` over `list`).
2.  **Decoupled Logic**: The `Snake` class is independent of `pygame`, allowing it to be unit-tested in environments without a GPU/Display.
3.  **Modern Tooling**: Leveraging `uv` for lightning-fast, reproducible dependency management.
4.  **Steelman Design**: Practicing the "Steelman" of tradeoffs—defending the strongest version of an alternative before rejecting it.

## 🛠 Features
- **Retro Aesthetic**: "Green-scale" color palette (`#9bbc0f`, `#0f380f`) and grid-based visuals mimicking the Nokia 3310.
- **Efficient Data Structures**: Uses `collections.deque` for $O(1)$ snake movement (adding a head, removing a tail).
- **Responsive Controls**: Optimized event loop handling for grid-snapped movement.

## 🚀 Getting Started
Ensure you have [uv](https://github.com/astral-sh/uv) installed.

### 1. Setup
```bash
uv sync
```

### 2. Run the Game
```bash
uv run src/main.py
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
- **Step 4: The Validation**: Check `tests/test_snake.py` to see how we verify game rules programmatically.

## 🧪 Customization & Exercises
This project is built to be modified. Here are some exercises to help you understand the code:

### 1. Change Key Bindings
Open `src/main.py` and find the `handle_input` method.
- **Challenge**: Replace `WASD` with `IJKL` keys.
- **Hint**: Look for `pygame.K_w`, `pygame.K_a`, `pygame.K_s`, `pygame.K_d` and change them to `pygame.K_i`, `pygame.K_j`, `pygame.K_k`, `pygame.K_l`.

### 2. Adjust Game Speed
In `src/main.py`, find the `update` method.
- **Challenge**: Make the game speed up faster.
- **Hint**: Change `if self.score % 50 == 0:` to a smaller number, like `20`.

### 3. Change the Palette
Find the "Colors" section at the top of `src/main.py`.
- **Challenge**: Change the "Nokia Green" to a "Cyberpunk Pink/Neon" theme.
- **Hint**: Update `COLOR_BG` and `COLOR_SNAKE` with new RGB values (e.g., `(255, 0, 255)`).

### 4. Modify the Grid
Change the `GRID_SIZE` constant.
- **Challenge**: Make the playing field much larger or smaller.
- **Hint**: Change `GRID_SIZE = 20` to `40`. Note how the rest of the game scales automatically!

## 🕹 Controls
- **WASD / Arrow Keys**: Move
- **R**: Restart (after Game Over)
- **Esc**: Quit
