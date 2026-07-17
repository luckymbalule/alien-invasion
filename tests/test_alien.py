import pytest
import math
from alien import Alien
from fleet import FleetDirection


@pytest.fixture
def alien_env(fake_game):
    alien = Alien(fake_game.screen, fake_game.settings)
    yield alien, fake_game.settings


# Test alien movement based on fleet state
@pytest.mark.parametrize(
    "direction", [FleetDirection.RIGHT, FleetDirection.LEFT]
)
def test_update_moves_alien_in_given_direction(direction, alien_env):
    alien, settings = alien_env
    expected_x = (
        alien.precise_x + (settings.alien_speed * direction)
    )

    alien.update(direction)
    
    assert math.isclose(alien.precise_x, expected_x)


def test_check_edges_when_alien_hits_right_edge_return_true(alien_env):
    alien, settings = alien_env
    alien.rect.right = settings.screen_width

    hit_edge = alien.check_edges()

    assert hit_edge is True


def test_check_edges_when_alien_hits_left_edge_return_true(alien_env):
    alien, _ = alien_env
    alien.rect.left = 0

    hit_edge = alien.check_edges()

    assert hit_edge is True


def test_check_edges_when_alien_inside_bounds_return_false(alien_env):
    alien, _ = alien_env
    alien.rect.center = alien.screen.get_rect().center

    hit_edge = alien.check_edges()

    assert hit_edge is False