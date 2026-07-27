"""Contains HealthSprite centralising health icon properties"""


import pygame
from asset_factory import load_image


class HealthSprite(pygame.sprite.Sprite):
    """Stores the rect and image of the health sprite"""

    IMAGE_PATH = "images/heart.png"

    def __init__(self, height: int):
        super().__init__()
        self.image = load_image(self.IMAGE_PATH, height)
        self.rect = self.image.get_rect()

    @classmethod
    def get_size(cls, height: int):
        image = load_image(cls.IMAGE_PATH, height)
        return image.get_rect().size