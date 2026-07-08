"""
Entry point for the game.
"""

import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from fleet import Fleet
from collision_system import CollisionSystem
from input_handler import InputHandler
from game_state import GameState


class AlienInvasion:
    """Orchestrates game components"""

    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")    
        self.clock = pygame.time.Clock()
        self.game_state = GameState(self.settings)
        self.ship = Ship(self.screen, self.settings)
        self.bullets = pygame.sprite.Group()
        self.fleet = Fleet(self.screen, self.settings)
        self.collision_system = CollisionSystem(self.bullets, self.fleet,
            self.ship, self.game_state, self.settings.screen_height)
        self._setup_input_handler() # An attempt at command pattern

    def run_game(self):
        while True:
            # Process user input events
            self._check_events()

            # Logic update phase
            if self.game_state.is_active:
                self.ship.update()
                self._update_bullets()
                self.fleet.update()
                self.collision_system.process_combat()
                fatal_collision = self.collision_system.process_penalties()
                if fatal_collision and self.game_state.is_active:
                    sleep(0.5)

            # Render phase
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond's to mouse and keypress events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                self.input_handler.handle_input(event)

    def _fire_bullets(self):
        if self.settings.bullet_active_limit > len(self.bullets):
            new_bullet = Bullet(self.screen, self.settings, self.ship.rect)
            self.bullets.add(new_bullet)

    def _setup_input_handler(self):
        """
        Configure key to action mapping.
        
        Initialise and instantiate the input handler.
        """
        keydown_map = {
            pygame.K_RIGHT: self.ship.start_moving_right,
            pygame.K_LEFT: self.ship.start_moving_left,
            pygame.K_SPACE: self._fire_bullets,
            pygame.K_q: sys.exit
        }
        keyup_map = {
            pygame.K_RIGHT: self.ship.stop_moving_right,
            pygame.K_LEFT: self.ship.stop_moving_left
        }

        self.input_handler = InputHandler(keydown_map, keyup_map)

    def _update_bullets(self):
        """Processes bullets' positions."""
        self.bullets.update()

        # Remove bullet if it reaches top of screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """Render to the display surface"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw()
        self.ship.blitme()
        self.fleet.draw()

        pygame.display.flip()


if __name__ == "__main__":
    # Instantiate and run the game
    ai = AlienInvasion()
    ai.run_game()