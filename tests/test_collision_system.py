import pytest
import pygame
from fleet import Fleet
from collision_system import CollisionSystem
from ship import Ship
from game_state import GameState

@pytest.fixture
def collision_env(mock_game):
    bullets = pygame.sprite.Group()
    fleet = Fleet(mock_game.screen, mock_game.settings)
    ship = Ship(mock_game.screen, mock_game.settings)
    game_state = GameState(mock_game.settings)
    collision_system = CollisionSystem(bullets, fleet, ship, game_state,
                                       mock_game.settings.screen_height)

    yield collision_system, mock_game.settings


def arrange_dirty_game_state(collision_sys):
    """Inject dummy items and offset ship position"""
    dummy_bullet = pygame.sprite.Sprite()
    dummy_bullet.rect = pygame.Rect((0,0), (1,1))
    collision_sys.bullets.add(dummy_bullet)
    collision_sys.ship.rect.x = 0
    collision_sys.ship.precise_x = 0.0

    return collision_sys.game_state.ships_remaining


def assert_reset_applied_on_game_end(collision_sys, initial_ships, settings):
    """Verifies all penalty resets are applied"""
    assert collision_sys.game_state.ships_remaining == initial_ships - 1
    assert len(collision_sys.bullets) == 0
    for alien in collision_sys.fleet.aliens:
        assert alien.rect.bottom < settings.screen_height
    
    center_x = settings.screen_width // 2
    assert collision_sys.ship.rect.centerx == center_x


def test_collision_system_resets_wave_state_on_extinction(collision_env):
    collision_sys, *_ = collision_env
    arrange_dirty_game_state(collision_sys)
    initial_alien_count = len(collision_sys.fleet.aliens)
    assert len(collision_sys.fleet.aliens) > 0
    assert len(collision_sys.bullets) > 0

    collision_sys.fleet.aliens.empty()
    collision_sys.process_combat()

    assert len(collision_sys.fleet.aliens) == initial_alien_count
    assert len(collision_sys.bullets) == 0


def test_collision_system_resets_screen_on_alien_hitting_bottom_edge(collision_env):
    collision_sys, settings = collision_env
    initial_ships = arrange_dirty_game_state(collision_sys)
    trigger_alien = collision_sys.fleet.aliens.sprites()[0]
    trigger_alien.rect.bottom = settings.screen_height

    collision_sys.process_penalties()

    assert_reset_applied_on_game_end(collision_sys, initial_ships, settings)


def test_collision_system_resets_screen_on_alien_hitting_ship(collision_env):
    collision_sys, settings = collision_env
    initial_ships = arrange_dirty_game_state(collision_sys)
    trigger_alien = collision_sys.fleet.aliens.sprites()[0]
    trigger_alien.rect.center = collision_sys.ship.rect.center

    collision_sys.process_penalties()

    assert_reset_applied_on_game_end(collision_sys, initial_ships, settings)