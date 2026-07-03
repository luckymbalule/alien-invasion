"""Contains Fleet class and FleetDirection enum."""

import pygame
from enum import IntEnum
from alien import Alien
from layout import col_layout, row_layout


class FleetDirection(IntEnum):
    RIGHT = 1
    LEFT = -1


class Fleet:
    """Represents an alien fleet"""

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.direction = FleetDirection.RIGHT
        self.aliens = pygame.sprite.Group()
        
        self.create()

    def create(self):
        """Spawns an alien fleet"""
        alien_w, alien_h = Alien.get_size(self.settings.alien_height)
        row = row_layout(
            scr_w=self.settings.screen_width,
            asset_w=alien_w
        )
        col = col_layout(
            scr_h=self.settings.screen_height,
            asset_h=alien_h,
            top=self.settings.hud_height,
            bottom=self.settings.ship_height,
            buf_rows=self.settings.alien_buffer_rows
        )

        y_end = col.start + (col.count * col.step)
        x_end = row.start + (row.count * row.step)

        for y_position in range(col.start, y_end, col.step):
            for x_position in range(row.start, x_end, row.step):
                self._add_alien(x_position, y_position)

    def draw(self):
        self.aliens.draw(self.screen)

    def update(self):
        """Public entry point to coordinate movement and direction"""
        for alien in self.aliens:
            alien.update(self.direction.value)
            
        if any(alien.check_edges() for alien in self.aliens):
            self._change_direction()

    def _add_alien(self, x_position, y_position):
        alien = Alien(self.screen, self.settings)
        alien.rect.topleft = (x_position, y_position)
        alien.precise_x = float(x_position)
        self.aliens.add(alien)

    def _change_direction(self):
        # self.aliens == self.aliens.sprites()
        # The former uses the Group's iterator to return a sprite()
        # Mwina kudabwa - kawelenge docs
        for alien in self.aliens:
            alien.rect.y += self.settings.fleet_drop_step
        
        # For future-self: Branchless state inversion is an option
        # Maybe just not here - wouldn't optimise perfomance apapa.
        if self.direction == FleetDirection.RIGHT:
            self.direction = FleetDirection.LEFT
        else:
            self.direction = FleetDirection.RIGHT