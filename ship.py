"""Defines the player's ship."""

import asset_factory

class Ship:
    """Represents a player's ship"""

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.screen_rect = self.screen.get_rect()

        # Cache ship surface
        image_path = "images/ship.png"
        self.image = asset_factory.load_image(
            image_path, self.settings.ship_height
        )
        self.rect = self.image.get_rect()

        # Start each ship image at center of screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store horizontal ship rect as a float
        self.precise_x = float(self.rect.x)

        # Flags to track movement; ship moves when flag is true.
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Transfer ship's image to it's current location"""
        self.screen.blit(self.image, self.rect)

    def start_moving_right(self):
        self.moving_right = True

    def stop_moving_right(self):
        self.moving_right = False

    def start_moving_left(self):
        self.moving_left = True

    def stop_moving_left(self):
        self.moving_left = False

    def update(self):
        """Update ship's position based on movement flags"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.precise_x += self.settings.ship_speed
        
        if self.moving_left and self.rect.left > 0:
            self.precise_x -= self.settings.ship_speed

        self.rect.x = self.precise_x