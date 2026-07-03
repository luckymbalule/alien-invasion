import pytest
import pygame
import math
from alien import Alien
from fleet import FleetDirection


@pytest.fixture
def alien_setup(mock_game):
    alien = Alien(mock_game.screen, mock_game.settings)
    yield alien, mock_game.settings


# Test alien movement based on fleet state
@pytest.mark.parametrize(
    "direction", [FleetDirection.RIGHT, FleetDirection.LEFT]
)
def test_alien_movement(direction, alien_setup):
    alien, settings = alien_setup
    start_x = alien.precise_x

    alien.update(direction)
    expected_x = (
        start_x + (settings.alien_speed * direction)
    )
    
    assert math.isclose(alien.precise_x, expected_x)


# Test edge checks
def test_alien_hits_right_edge_return_true(alien_setup):
    alien, settings = alien_setup
    alien.rect.right = settings.screen_width
    assert alien.check_edges() is True


def test_alien_hits_left_edge_return_true(alien_setup):
    alien, _ = alien_setup
    alien.rect.left = 0
    assert alien.check_edges() is True


def test_alien_inside_bounds_return_false(alien_setup):
    alien, _ = alien_setup
    alien.rect.center = alien.screen.get_rect().center
    assert alien.check_edges() is False