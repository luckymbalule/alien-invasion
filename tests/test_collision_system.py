import pytest
import pygame
from fleet import Fleet
from collision_system import CollisionSystem

@pytest.fixture
def collision_env(mock_game):
    bullets = pygame.sprite.Group()
    fleet = Fleet(mock_game.screen, mock_game.settings)
    collision_system = CollisionSystem(bullets, fleet)

    yield collision_system, mock_game.settings


def test_collision_system_resets_wave_state_on_extinction(collision_env):
    collision_system, *_ = collision_env
    dummy_bullet = pygame.sprite.Sprite()
    dummy_bullet.rect = pygame.Rect((0,0), (1,1))
    collision_system.bullets.add(dummy_bullet)
    assert len(collision_system.fleet.aliens) > 0
    assert len(collision_system.bullets) > 0

    collision_system.fleet.aliens.empty()
    collision_system.update()

    assert len(collision_system.fleet.aliens) > 0
    assert len(collision_system.bullets) == 0