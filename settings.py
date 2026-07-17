"""Defines settings data class"""

from dataclasses import dataclass


@dataclass
class Settings:
    """Represents game settings data"""
    screen_width: int = 480
    screen_height: int = 640
    bg_color: tuple = (42, 42, 42)
    font: str | None = None

    # Alien settings
    alien_height: int = 35
    alien_buffer_rows: int = 3
    alien_speed: float = 1.0

    # Button settings
    button_width: int = 250
    button_height: int = 60 
    button_font_size: int = 32
    button_color: tuple = (42, 42, 42)
    button_color_disabled: tuple = (120, 125, 113)
    button_bg_color: tuple = (242, 239, 233)
    button_bg_color_disabled: tuple = (201, 206, 189)
    button_spacing: int = 20

    # Bullet settings
    bullet_speed: float = 2.5
    bullet_width : int = 3
    bullet_height: int = 15
    bullet_color: tuple = (247, 240, 82)
    bullet_active_limit: int = 4

    # Fleet settings
    fleet_drop_step: int = 20

    # HUD settings
    hud_height: int = 60

    # Menu settings
    menu_bg_color: tuple = (42, 42, 42)
    menu_bg_dim: int = 164
    menu_bg_solid: int = 255

    # Ship settings
    ship_height: int = 30
    ship_speed: float = 1.5
    ship_limit: int = 3