"""Defines settings data class"""

from dataclasses import dataclass


@dataclass
class Settings:
    """Represents game settings data"""
    screen_width: int = 900
    screen_height: int = 600
    bg_color: tuple = (42, 42, 42)

    # Ship settings
    ship_height: int = 30
    ship_speed: float = 1.5

    # Bullet settings
    bullet_speed: float = 2.5
    bullet_width : int = 3
    bullet_height: int = 15
    bullet_color: tuple = (247, 240, 82)
    bullet_active_limit: int = 5

    # Alien settings
    alien_height: int = 40
    alien_buffer_rows: int = 3
    alien_speed: float = 1.0

    # Fleet settings
    fleet_drop_step: int = 20

    # HUD settings
    hud_height: int = 50