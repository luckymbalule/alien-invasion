"""Centralise menu overlay, button layout, and mouse-target action mapping"""


import pygame
from settings import Settings
from button import Button, ButtonConfig
from layout import stack_vertical


class Menu:
    """A fullscreen dimmable menu that lazily builds its buttons"""

    def __init__(self, screen: pygame.Surface, settings: Settings,
        dim_overlay=True
    ):
        self.buttons: list[Button] = []
        self.screen = screen
        self.settings = settings
        overlay_alpha = (
            self.settings.menu_bg_dim if dim_overlay
            else self.settings.menu_bg_solid
        ) 
        self.overlay = pygame.Surface(
            (self.settings.screen_width, self.settings.screen_height),
            pygame.SRCALPHA
        )
        self.overlay.fill((*self.settings.menu_bg_color, overlay_alpha))

    def build(self, configs: list[ButtonConfig]):
        """
        Create buttons in a vertically stacked layout
        
        Return False if invalid arg.
        """
        if (
            not isinstance(configs, list)
            or not configs 
            or not all(isinstance(config, ButtonConfig) for config in configs)
        ):
            raise TypeError("Configs should be a list of ButtonConfig(s)")
        
        button_positions = stack_vertical(
            position=self.screen.get_rect().center,
            item_h=self.settings.button_height,
            item_w=self.settings.button_width,
            count=len(configs),
            step=self.settings.button_spacing
        )

        for button_config, position in zip(configs, button_positions):
            self.buttons.append(
                Button(self.screen, self.settings, button_config, position)
            )

    def draw(self):
        """Blit overlay and buttons to screen"""
        self.screen.blit(self.overlay, (0, 0))
        for button in self.buttons:
            button.draw()
    
    def get_mouse_targets(self):
        """Return a list of filtered active buttons (rect, action) pairs"""
        return [
            (button.rect, button.action) for button in self.buttons
            if button.is_enabled and button.action
        ]