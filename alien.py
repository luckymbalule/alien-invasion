"""
Contains the alien entities and behaviour.
"""

import asset_factory
from pygame.sprite import Sprite


class Alien(Sprite):
    """Represents an alien"""

    IMAGE_PATH = "images/alien.png"

    def __init__(self, screen, settings, difficulty):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.difficulty = difficulty

        # Cache image to optimise performance
        self.image = asset_factory.load_image(
            self.IMAGE_PATH, self.settings.alien_height
        )
        self.rect = self.image.get_rect()

        # Store exact position which can be a float 
        # depending on speed calculations
        self.precise_x: float = float(self.rect.x) 

    @classmethod
    def get_size(cls, height):
        """Get alien rect size without creating instantiating alien"""
        surface = asset_factory.load_image(cls.IMAGE_PATH, height)
        return surface.get_rect().size

    def check_edges(self):
        """Return bool on reaching either display edge"""
        return (
            self.rect.left <= 0 
            or self.rect.right >= self.settings.screen_width
        )

    def update(self, direction_multiplier: int):
        """Update alien position based on speed and direction"""
        self.precise_x += (
            self.difficulty.alien_speed * direction_multiplier
        )
        self.rect.x = self.precise_x