"""
Manages the player's ship and movement

This module contains Ship class for rendering and state management, and
the ShipDirection enum for standardised directions
"""

import asset_factory
from enum import Enum


class ShipDirection(Enum):
    RIGHT = "Right"
    LEFT = "Left"
    STATIONARY = "Stationary"


class Ship:
    """
    Manages the player's ship tracking position, direction, and handling
    screen collisions
    """

    def __init__(self, screen, settings, difficulty):
        self.screen = screen
        self.settings = settings
        self.difficulty = difficulty
        self.screen_rect = self.screen.get_rect()

        # Cache ship surface
        image_path = "images/ship.png"
        self.image = asset_factory.load_image(
            image_path, self.settings.ship_height
        )
        self.rect = self.image.get_rect()
        self.reset()

    def blitme(self):
        """Transfer ship's image to it's current location"""
        self.screen.blit(self.image, self.rect)

    def start_moving_right(self):
        self.direction = ShipDirection.RIGHT

    def stop_moving_right(self):
        self.direction = ShipDirection.STATIONARY

    def start_moving_left(self):
        self.direction = ShipDirection.LEFT

    def stop_moving_left(self):
        self.direction = ShipDirection.STATIONARY

    def reset(self):
        self.direction = ShipDirection.STATIONARY
        self.rect.midbottom = self.screen_rect.midbottom
        self.precise_x = float(self.rect.x)

    def update(self):
        """Update ship's position based on movement flag"""
        match self.direction:
            case ShipDirection.RIGHT:
                if self.rect.right < self.screen_rect.right:
                    self.precise_x += self.difficulty.ship_speed
            case ShipDirection.LEFT:
                if self.rect.left > 0:
                    self.precise_x -= self.difficulty.ship_speed

        self.rect.x = self.precise_x