"""
Contains CollisionSystem class to orchestrate all cross-domain
interactions in one place
"""

import pygame


class CollisionSystem:
    """Manage all cross-domain interactions"""

    def __init__(self, bullets, fleet):
        self.bullets = bullets
        self.fleet = fleet

    def update(self):
        """Coordinate interactions - public entry point"""
        self._handle_aliens_bullets_collisions()

    def _handle_aliens_bullets_collisions(self):
        """Processes alien and bullets collisions"""
        pygame.sprite.groupcollide(
            self.bullets, self.fleet.aliens, True, True
        )

        if not self.fleet.aliens:
            self.bullets.empty()
            self.fleet.create()