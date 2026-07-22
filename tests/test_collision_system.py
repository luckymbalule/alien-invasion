import pytest
import pygame
from collision_system import CollisionSystem
from game_state import GamePhase

@pytest.fixture
def collision_env(fake_game):
    bullets = pygame.sprite.Group()
    collision_system: CollisionSystem = CollisionSystem(
        bullets,
        fake_game.fleet,
        fake_game.ship,
        fake_game.game_state,
        fake_game.difficulty,
        fake_game.settings.screen_height
    )

    return collision_system, fake_game.ship, fake_game.settings


def test_process_penalties_when_alien_hits_bottom_edge_reset_combat_state(
    collision_env
):
    collision_sys, ship, settings = collision_env
    collision_sys.game_state.phase = GamePhase.PLAYING
    collision_sys.bullets.add(pygame.sprite.Sprite())
    alien = collision_sys.fleet.aliens.sprites()[0]
    alien.rect.bottom = settings.screen_height
    initial_alien_count = len(collision_sys.fleet.aliens)

    critical = collision_sys.process_penalties()

    assert len(collision_sys.bullets) == 0
    assert collision_sys.ship.rect.centerx == settings.screen_width // 2
    assert len(collision_sys.fleet.aliens) == initial_alien_count
    assert critical is True


def test_process_penalties_when_alien_hits_last_ship_update_phase(
    collision_env
):
    collision_sys, *_ = collision_env
    collision_sys.game_state.phase = GamePhase.PLAYING
    collision_sys.game_state.ships_remaining = 1
    del collision_sys.fleet.aliens.sprites()[1:]
    alien = collision_sys.fleet.aliens.sprites()[0]
    alien.rect.center = collision_sys.ship.rect.center

    critical = collision_sys.process_penalties()

    assert collision_sys.game_state.phase == GamePhase.GAME_OVER
    assert critical is True


def test_process_penalties_when_no_hits_update_nothing(
    collision_env
):
    collision_sys, *_ = collision_env
    collision_sys.game_state.phase = GamePhase.PLAYING
    collision_sys.bullets.add(pygame.sprite.Sprite())
    initial_alien_count = len(collision_sys.fleet.aliens)

    critical = collision_sys.process_penalties()

    assert len(collision_sys.bullets) == 1
    assert len(collision_sys.fleet.aliens) == initial_alien_count
    assert critical is False


def test_process_combat_when_bullet_hits_alien_removes_both(
    collision_env
):
    collision_sys, *_ = collision_env
    for _ in range(2):
        collision_sys.bullets.add(pygame.sprite.Sprite())
    collision_sys.bullets.sprites()[0].rect = pygame.Rect((0,0), (1,1))
    collision_sys.bullets.sprites()[1].rect = pygame.Rect((20,10), (1,1))
    collision_sys.fleet.aliens.sprites()[0].rect.topleft = (0,0)
    collision_sys.fleet.aliens.sprites()[1].rect.topleft = (50,50)
    initial_alien_count = len(collision_sys.fleet.aliens)
    assert len(collision_sys.bullets) == 2

    collision_sys.process_combat()

    assert len(collision_sys.fleet.aliens) == initial_alien_count - 1
    assert len(collision_sys.bullets) == 1


def test_process_combat_when_bullet_hits_last_alien_resets_combat_state(
    collision_env
):
    collision_sys, _, settings = collision_env
    collision_sys.bullets.add(pygame.sprite.Sprite())
    collision_sys.bullets.sprites()[0].rect = pygame.Rect((0,0), (1,1))
    initial_alien_count = len(collision_sys.fleet.aliens)
    removal_list = collision_sys.fleet.aliens.sprites()[1:]
    collision_sys.fleet.aliens.remove(removal_list)
    collision_sys.fleet.aliens.sprites()[0].rect.topleft = (0,0)

    collision_sys.process_combat()

    assert len(collision_sys.bullets) == 0
    assert collision_sys.ship.rect.centerx == settings.screen_width // 2
    assert len(collision_sys.fleet.aliens) == initial_alien_count