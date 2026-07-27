"""Manages HUD rendering and game state displays"""


import pygame
from health_sprite import HealthSprite


class ScoreBoard:
    """
    Prepares and renders game metrics (level, lives, score) to the display
    """
    def __init__(self, settings, screen, game_state, difficulty):
        self.settings = settings
        self.screen = screen
        self.game_state = game_state
        self.difficulty = difficulty

        self.font = pygame.font.SysFont(
            self.settings.font,
            self.settings.hud_font_size,
        )

        self.health_count = None

    def draw(self):
        """Renders game metrics to the display"""
        self._prep_health()
        self._prep_level()
        self._prep_score()

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.health_group.draw(self.screen)

    def _prep_health(self):
        if self.health_count != self.game_state.ships_remaining:
            self._create_health()

    def _prep_level(self):
        level_str = f"Level: {self.difficulty.level}"
        self.level_image = self.font.render(
            level_str, True, self.settings.hud_color
        )
        self.level_rect = self.level_image.get_rect()
        self.level_rect.centery = self.settings.hud_height // 2
        self.level_rect.left = self.settings.hud_margin

    def _prep_score(self):
        score_str = f"Score: {self.game_state.score:,}"
        self.score_image = self.font.render(
            score_str, True, self.settings.hud_color
        )
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centery = self.settings.hud_height // 2
        self.score_rect.right = (
            self.settings.screen_width - self.settings.hud_margin
        )

    def _create_health(self):
        """Creates and positions the health icons"""
        self.health_group = pygame.sprite.Group()
        self.health_count = self.game_state.ships_remaining
        height = self.settings.hud_asset_height
        spacing = self.settings.hud_asset_spacing

        # Expression: (width * N) + spacing * (N - 1)
        width, _ = HealthSprite.get_size(height)
        assets_width = width * self.health_count
        spacing_width = spacing * (self.health_count - 1)
        container_width =  max(0, assets_width + spacing_width)

        start_x = self.screen.get_rect().centerx - (container_width // 2)

        for i in range(self.health_count):
            health = HealthSprite(height)
            health.rect.centery = self.settings.hud_height // 2
            health.rect.x = (start_x + (i * (spacing + width)))

            self.health_group.add(health)