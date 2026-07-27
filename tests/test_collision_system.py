import pytest
import pygame
from collision_system import CollisionSystem
from game_state import GamePhase

@pytest.fixture
def collision_env(fake_game):
    bullets = pygame.sprite.Group()
    for _ in range(2):
        bullet = pygame.sprite.Sprite()
        bullet.rect = pygame.Rect((0, 0), (1, 1))
        bullets.add(bullet)

    collision_system: CollisionSystem = CollisionSystem(
        bullets,
        fake_game.fleet,
        fake_game.ship,
        fake_game.game_state,
        fake_game.difficulty,
        fake_game.settings
    )
    collision_system.game_state.phase = GamePhase.PLAYING

    return collision_system, fake_game.ship, fake_game.settings


def test_process_penalties_when_alien_hits_bottom_edge_reset_combat_state(
    collision_env
):
    collision_sys, _, settings = collision_env
    alien = collision_sys.fleet.aliens.sprites()[0]
    alien.rect.bottom = settings.screen_height
    initial_alien_count = len(collision_sys.fleet.aliens)

    critical = collision_sys.process_penalties()

    assert len(collision_sys.bullets) == 0
    assert collision_sys.ship.rect.centerx == settings.screen_width // 2
    assert len(collision_sys.fleet.aliens) == initial_alien_count
    assert critical is True


def test_process_penalties_when_last_ship_lost_transition_phase(
    collision_env
):
    collision_sys, *_ = collision_env
    collision_sys.game_state.ships_remaining = 1
    alien = collision_sys.fleet.aliens.sprites()[0]
    alien.rect.center = collision_sys.ship.rect.center

    critical = collision_sys.process_penalties()

    assert collision_sys.game_state.phase == GamePhase.GAME_OVER
    assert critical is True


def test_process_penalties_when_no_hits_update_nothing(
    collision_env
):
    collision_sys, *_ = collision_env
    initial_alien_count = len(collision_sys.fleet.aliens)

    critical = collision_sys.process_penalties()

    assert len(collision_sys.bullets) == 2
    assert len(collision_sys.fleet.aliens) == initial_alien_count
    assert critical is False


def test_process_combat_when_bullet_hits_alien_removes_both_and_awards_points(
    collision_env
):
    collision_sys, *_ = collision_env
    target_bullet = collision_sys.bullets.sprites()[0]
    target_bullet.rect.topleft = (10,10)
    collision_sys.fleet.aliens.sprites()[0].rect.topleft = (10,10)
    initial_alien_count = len(collision_sys.fleet.aliens)
    collision_sys.difficulty.level = 2
    collision_sys.game_state.score = 50

    collision_sys.process_combat()

    assert len(collision_sys.fleet.aliens) == initial_alien_count - 1
    assert target_bullet not in collision_sys.bullets
    assert collision_sys.game_state.score == 60


def test_process_combat_when_last_alien_destroyed_resets_combat_state(
    collision_env
):
    collision_sys, _, settings = collision_env
    collision_sys.difficulty.level = 3
    collision_sys.game_state.score = 85
    initial_alien_count = len(collision_sys.fleet.aliens)
    removal_list = collision_sys.fleet.aliens.sprites()[1:]
    collision_sys.fleet.aliens.remove(removal_list)
    collision_sys.fleet.aliens.sprites()[0].rect.topleft = (20,20)
    collision_sys.bullets.sprites()[0].rect.topleft = (20,20)

    collision_sys.process_combat()

    assert collision_sys.difficulty.level == 4
    assert collision_sys.game_state.score == 85 + (settings.alien_points * 3)
    assert len(collision_sys.bullets) == 0
    assert collision_sys.ship.rect.centerx == settings.screen_width // 2
    assert len(collision_sys.fleet.aliens) == initial_alien_count


def test_process_combat_when_no_collisions_update_nothing(
    collision_env
):
    collision_sys, *_ = collision_env
    initial_alien_count = len(collision_sys.fleet.aliens)
    collision_sys.game_state.score = 100
    collision_sys.difficulty.level = 5

    collision_sys.process_combat()

    assert len(collision_sys.bullets) == 2
    assert len(collision_sys.fleet.aliens) == initial_alien_count
    assert collision_sys.game_state.score == 100
    assert collision_sys.difficulty.level == 5