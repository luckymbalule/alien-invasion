"""
Centralise collision logic to orchestrate all cross-domain interactions
"""

import pygame
from game_state import GamePhase


class CollisionSystem:
    """
    Store bullets, fleet, ship, game state and process all cross-domain
    interactions
    """

    def __init__(
        self, bullets, fleet, ship, game_state, difficulty,
        screen_height
    ):
        self.screen_height = screen_height
        self.bullets = bullets
        self.fleet = fleet
        self.ship = ship
        self.game_state = game_state
        self.difficulty = difficulty

    def process_combat(self):
        """Responds to alien and bullet collisions"""
        pygame.sprite.groupcollide(
            self.bullets, self.fleet.aliens, True, True
        )

        if not self.fleet.aliens:
            self.bullets.empty()
            self.fleet.create()
            self.difficulty.update()

    def process_penalties(self):
        """Responds to collisions requiring a penalty to player"""
        if any(alien.rect.bottom >= self.screen_height
               for alien in self.fleet.aliens
        ) or pygame.sprite.spritecollideany(self.ship, self.fleet.aliens):
            self._ship_hit()
            return True
        return False

    def _ship_hit(self):
        self.game_state.register_ship_loss()
        if self.game_state.phase == GamePhase.PLAYING:
            self.bullets.empty()
            self.fleet.reset()
            self.ship.reset()