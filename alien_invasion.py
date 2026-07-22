"""
Entry point for Alien Invasion.
"""

import sys
import pygame
from time import sleep
from bullet import Bullet
from button import ButtonConfig
from collision_system import CollisionSystem
from difficulty import Difficulty
from fleet import Fleet
from game_state import GameState, GamePhase
from input_handler import InputHandler
from menu import Menu
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Orchestrate game components"""

    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")
        self.difficulty = Difficulty(self.settings)
        self.game_state = GameState(self.settings)
        self.clock = pygame.time.Clock()
        self.ship = Ship(self.screen, self.settings, self.difficulty)
        self.bullets = pygame.sprite.Group()
        self.fleet = Fleet(self.screen, self.settings, self.difficulty)
        self.collision_system = CollisionSystem(
            self.bullets,
            self.fleet,
            self.ship,
            self.game_state,
            self.difficulty,
            self.settings.screen_height
        )

        self._setup_static_key_bindings()
        self._setup_menus()
        self.game_state.subscribe(self._on_phase_transition)
        self._on_phase_transition(self.game_state.phase)

    def run_game(self):
        while True:
            # Process input events
            self._check_events()

            # Logic update phase
            if self.game_state.phase == GamePhase.PLAYING:
                self.ship.update()
                self._update_bullets()
                self.fleet.update()
                self.collision_system.process_combat()
                critical_collision = self.collision_system.process_penalties()
                if (
                    critical_collision
                    and self.game_state.phase == GamePhase.PLAYING
                ):
                    sleep(0.5)

            # Render phase
            self._update_screen()
            self.clock.tick(60)        

    def _check_events(self):
        """Responds to mouse and keypress events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                self.input_handler.handle_input(event)

    def _fire_bullets(self):
        if self.settings.bullet_active_limit > len(self.bullets):
            new_bullet = Bullet(
                self.screen,
                self.settings,
                self.difficulty,
                self.ship.rect
            )
            self.bullets.add(new_bullet)

    def _on_phase_transition(self, phase):
        """Rebuilds dynamic key bindings and active menu for the new phase"""
        menu_phase_map = {
            GamePhase.MENU: self.main_menu,
            GamePhase.PAUSED: self.paused_menu,
            GamePhase.GAME_OVER: self.game_over_menu,
        }

        match phase:
            case GamePhase.PLAYING:
                self.active_menu = []
                self.keydown_map[pygame.K_z] = self._fire_bullets
                self.keydown_map.pop(pygame.K_RETURN, None)
                self.keydown_map[pygame.K_ESCAPE] = self.game_state.pause
            case GamePhase.PAUSED:
                self.active_menu = menu_phase_map[phase]
                self.keydown_map[pygame.K_z] = self.game_state.resume
                self.keydown_map[pygame.K_RETURN] = self.game_state.resume
                self.keydown_map[pygame.K_ESCAPE] = self.game_state.resume
            case GamePhase.MENU:
                self.active_menu = menu_phase_map[phase]
                self.keydown_map[pygame.K_z] = self._start_game
                self.keydown_map[pygame.K_RETURN] = self._start_game
                self.keydown_map[pygame.K_ESCAPE] = sys.exit
            case GamePhase.GAME_OVER:
                self.active_menu = menu_phase_map[phase]
                self.keydown_map.pop(pygame.K_z, None)
                self.keydown_map[pygame.K_RETURN] = self._start_game
                self.keydown_map[pygame.K_ESCAPE] = self._return_to_menu

        mouse_targets = (
            [] if phase == GamePhase.PLAYING
            else self.active_menu.get_mouse_targets()
        )

        self.input_handler = InputHandler(
            self.keydown_map, self.keyup_map, mouse_targets
        )

    def _return_to_menu(self):
        if self.game_state.phase in (GamePhase.GAME_OVER, GamePhase.PAUSED):
            self.game_state.reset()
            self.difficulty.reset()
            self.bullets.empty()
            self.fleet.reset()
            self.ship.reset()

    def _start_game(self):
        if self.game_state.phase == GamePhase.PLAYING:
            return
        
        self.game_state.reset()
        self.game_state.start()
        self.difficulty.reset()
        self.bullets.empty()
        self.fleet.reset()
        self.ship.reset()

    def _setup_menus(self):
        """Initialise menu instances and build them"""
        main_menu = [
            ButtonConfig("Play", action=self._start_game),
            ButtonConfig("High Scores", False),
            ButtonConfig("Settings", False),
            ButtonConfig("Quit", action=sys.exit),
        ]
        paused_menu = [
            ButtonConfig("Resume", action=self.game_state.resume),
            ButtonConfig("New Game", action=self._start_game),
            ButtonConfig("Main Menu", action=self._return_to_menu),
            ButtonConfig("Quit", action=sys.exit),
        ]
        game_over_menu = [
            ButtonConfig("Retry", action=self._start_game),
            ButtonConfig("Main Menu", action=self._return_to_menu),
            ButtonConfig("Quit", action=sys.exit)
        ]

        self.main_menu = Menu(self.screen, self.settings, dim_overlay=False)
        self.main_menu.build(main_menu)

        self.paused_menu = Menu(self.screen, self.settings)
        self.paused_menu.build(paused_menu)

        self.game_over_menu = Menu(self.screen, self.settings)
        self.game_over_menu.build(game_over_menu)

    def _setup_static_key_bindings(self):
        """Initialises static key - action mappings"""
        self.keydown_map = {
            pygame.K_RIGHT: self.ship.start_moving_right,
            pygame.K_LEFT: self.ship.start_moving_left,
            pygame.K_q: sys.exit
        }

        self.keyup_map = {
            pygame.K_RIGHT: self.ship.stop_moving_right,
            pygame.K_LEFT: self.ship.stop_moving_left
        }

    def _update_bullets(self):
        self.bullets.update()

        # Remove bullet if it exceeds top edge
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """Renders to the screen surface"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw()
        self.ship.blitme()
        self.fleet.draw()

        if self.game_state.phase != GamePhase.PLAYING:
            self.active_menu.draw()

        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()