# Architecture Decision Records (ADR)

## ADR 1: Game Library Selection

### Status
Accepted

### Context
We need a Python library to handle windowing, graphics, and user input for a Nokia-style Snake game. Candidates include `pygame`, `curses`, `turtle`, and `tkinter`.

### Decision
We will use `pygame`.

### Rationale
- **Performance**: `pygame` handles frame rates and sprite-based rendering more efficiently than `turtle` or `tkinter`.
- **Input Handling**: Superior event loop for responsive controls (critical for Snake).
- **Retro Aesthetic**: Easy to implement pixel-perfect grid rendering and "green-scale" color palettes to mimic the Nokia 3310 screen.
- **Portability**: Works across Windows, macOS, and Linux without complex terminal dependencies (unlike `curses` on Windows).

### Steelman Design Tradeoffs
- **Against `curses`**: While `curses` offers a more "authentic" terminal-based feel, it is notoriously difficult to set up on Windows and lacks easy support for custom fonts/colors that mimic the physical hardware's look.
- **Against `turtle`**: `turtle` is simple but its drawing model is vector-based and slow for a dynamic game loop.
- **Against `tkinter`**: `tkinter` is part of the standard library, but its `Canvas` widget is not optimized for game loops and lacks the robust audio/input utilities of `pygame`.

---

## ADR 2: Data Structure for Snake Body

### Status
Accepted

### Context
How to store and manipulate the snake's segments as it grows and moves.

### Decision
We will use a `collections.deque` (double-ended queue) of coordinate tuples `(x, y)`.

### Rationale
- **Efficiency**: Moving the snake involves adding a new head and removing the tail. A `deque` provides $O(1)$ time complexity for both `appendleft` and `pop`.
- **Readability**: Naturally maps to the behavior of a moving line.

### Steelman Design Tradeoffs
- **Against `list`**: Popping from the start of a `list` is $O(n)$ as all other elements must be shifted. For very long snakes, this could theoretically impact performance, though negligible for this scale. `deque` is semantically more correct.

---

## ADR 3: Game Loop and Timing

### Status
Accepted

### Context
How to manage game speed and updates.

### Decision
Fixed-rate update loop using `pygame.time.Clock`.

### Rationale
- Mimics the "stepped" movement of the original Nokia game.
- Simplifies collision detection (only check on "ticks").

### Steelman Design Tradeoffs
- **Against Variable Delta Time**: While modern games use delta-time for smooth movement, the "Nokia" feel *requires* discrete, grid-based steps. Interpolation would ruin the aesthetic.

---

## ADR 4: Dependency Management and Project Tooling

### Status
Accepted

### Context
Modern Python packaging is moving toward `pyproject.toml` as the standard. We need a tool that is fast, reliable, and handles project-level environments easily.

### Decision
We will use `uv` and maintain a `pyproject.toml`.

### Rationale
- **Speed**: `uv` is significantly faster than `pip`.
- **Reproducibility**: `uv` generates a lockfile by default, ensuring all environments are identical.
- **Project Isolation**: `uv sync` and `uv run` simplify the process of managing virtual environments without manual activation.

### Steelman Design Tradeoffs
- **Against `pip` with `requirements.txt`**: While `pip` is the ubiquitous standard, it doesn't handle project metadata as cleanly as `pyproject.toml` and lacks a built-in lockfile mechanism without extra tooling like `pip-compile`. `uv` provides a more cohesive "all-in-one" experience for developers.
- **Against `poetry`**: `poetry` is a strong alternative but `uv` is significantly faster and more lightweight, which fits the "simple retro game" scope better.
