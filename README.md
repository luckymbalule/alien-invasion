# Alien Invasion

A pygame-ce implementation of the arcade shooter from Python Crash Course (3rd Edition) by Eric Matthes.

This has been built with deliberate intentions to serve as a sandbox for implementing software design patterns, algebraic layout logic, and Test-Driven Development (TDD) in an interactive game.

## Description
In Alien Invasion, a player controls a rocket ship that is anchored to the bottom of the screen. The player can move the rocket ship left or right using arrow keys and shoot using spacebar.
When the game begins a fleet of aliens fills the atmosphere [top of screen] and move down the screen. The player shoots and destroys aliens. If the player shoots/destroys all aliens, a new fleet fills the sky that moves faster than the previous fleet. If an alien hits the player's ship or the bottom of the screen, the player loses a ship. If a player loses three ships, the game ends.

## Controls
[#controls](#controls)

- **Q** — Quit the game at any time
- **Left / Right arrows** — Move the ship left and right
- **Z** — Fire bullets (Playing); start game (Main Menu); resume game (Pause Menu)
- **Enter/Return** — Start game (Main Menu); retry (Game Over); resume game (Pause Menu)
- **Esc** — Pause game (Playing); resume game (Pause Menu); return to main menu (Game Over); quit game (Main Menu)
- **Mouse** — click any menu button directly

## Run
```bash
pip install pygame-ce
python alien_invasion.py
```

## Test
```bash
pip install pytest
pytest
```