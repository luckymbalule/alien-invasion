"""
Contain general button configuration, and button behaviour
"""

import pygame
from dataclasses import dataclass
from typing import Optional, Callable


@dataclass
class ButtonConfig:
    label: str
    is_enabled: bool = True
    action: Optional[Callable] = None


class Button:
    """Store button position, state, action, and label"""

    def __init__(self, screen, settings, config: ButtonConfig, position):
        self.screen = screen
        self.settings = settings
        self.label = config.label
        self.is_enabled = config.is_enabled
        self.action = config.action
        self.position = position

        if self.is_enabled:
            self.color = self.settings.button_color
            self.bg_color = self.settings.button_bg_color
        else:
            self.color = self.settings.button_color_disabled
            self.bg_color = self.settings.button_bg_color_disabled

        self.rect = pygame.Rect(
            (0,0), (self.settings.button_width, self.settings.button_height)
        )
        self.rect.topleft = self.position

        self._prep_label()

    def draw(self):
        """Blit button label and rect fill"""
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)

    def _prep_label(self):
        """Render and position label to rect"""
        self.font = pygame.font.SysFont(
            self.settings.font, self.settings.button_font_size
        )
        self.message_image = self.font.render(
            self.label,True, self.color, self.bg_color
        )
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center