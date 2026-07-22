"""
Contains bullet sprite used by the game
"""

import pygame


class Bullet(pygame.sprite.Sprite):
    """Represents bullet sprite"""

    def __init__(self, screen, settings, difficulty, ship_rect):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.difficulty = difficulty
        self.ship_rect = ship_rect
        self.rect = pygame.Rect(
            (0, 0),
            (self.settings.bullet_width, self.settings.bullet_height)
        )
        self.rect.midtop = self.ship_rect.midtop

        # Store exact vertical point of the bullet
        self.precise_y = float(self.rect.y)

    def draw(self):
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)

    def update(self):
        """Process bullet movement"""
        self.precise_y -= self.difficulty.bullet_speed
        self.rect.y = self.precise_y