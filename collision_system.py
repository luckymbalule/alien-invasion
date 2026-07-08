"""
Contains CollisionSystem class to orchestrate all cross-domain
interactions in one place
"""

import pygame


class CollisionSystem:
    """Manage all cross-domain interactions"""

    def __init__(self, bullets, fleet, ship, game_state, screen_height):
        self.screen_height = screen_height
        self.bullets = bullets
        self.fleet = fleet
        self.ship = ship
        self.game_state = game_state

    def process_combat(self):
        """Responds to alien and bullet collisions"""
        pygame.sprite.groupcollide(
            self.bullets, self.fleet.aliens, True, True
        )

        if not self.fleet.aliens:
            self.bullets.empty()
            self.fleet.create()

    def process_penalties(self):
        """Responds to alien [screen, ship] collisions"""
        if any(alien.rect.bottom >= self.screen_height
               for alien in self.fleet.aliens
        ) or pygame.sprite.spritecollideany(self.ship, self.fleet.aliens):
            self._ship_hit()
            return True
        return False

    def _ship_hit(self):
        if self.game_state.ships_remaining > 0:
            self.game_state.ships_remaining -= 1
            self.bullets.empty()
            self.fleet.reset()
            self.ship.reset()
        else:
            self.game_state.is_active = False