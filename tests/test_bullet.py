import pytest
import pygame
from bullet import Bullet


@pytest.fixture
def bullet_env(fake_game):
    bullet_group = pygame.sprite.Group()
    for _ in range(2):
        bullet = Bullet(
            fake_game.screen,
            fake_game.settings,
            fake_game.difficulty,
            fake_game.ship.rect
        )
        bullet_group.add(bullet)

    return bullet_group, fake_game.difficulty.bullet_speed


def test_update_when_bullet_in_bound_moves_bullet(bullet_env):
    bullets, speed = bullet_env
    initial_x_positions = [sprite.rect.x for sprite in bullets]
    initial_y_positions = [sprite.precise_y for sprite in bullets]
    expected_y_positions = [y - speed for y in initial_y_positions]

    bullets.update()

    current_x_positions = [sprite.rect.x for sprite in bullets]
    current_y_positions = [sprite.precise_y for sprite in bullets]

    assert current_y_positions == expected_y_positions
    assert current_x_positions == initial_x_positions


def test_update_when_bullet_exceeds_edge_removes_bullet(bullet_env):
    bullets, *_ = bullet_env
    target_bullet = bullets.sprites()[0]
    target_bullet.precise_y = -target_bullet.rect.height

    bullets.update()

    assert target_bullet not in bullets