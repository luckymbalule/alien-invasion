import pytest
from ship import ShipDirection


@pytest.fixture
def ship_env(fake_game):
    return fake_game.ship, fake_game.difficulty.ship_speed

def test_update_when_direction_right_moves_ship_right(ship_env):
    ship, speed = ship_env
    ship.direction = ShipDirection.RIGHT
    current_x = ship.precise_x

    ship.update()
    
    assert ship.precise_x == current_x + speed


def test_update_when_direction_left_moves_ship_left(ship_env):
    ship, speed = ship_env
    ship.direction = ShipDirection.LEFT
    current_x = ship.precise_x

    ship.update()
    
    assert ship.precise_x == current_x - speed


def test_update_when_direction_stationary_ship_stays_stationary(ship_env):
    ship, *_ = ship_env
    ship.direction = ShipDirection.STATIONARY
    current_x = ship.precise_x

    ship.update()
    
    assert ship.precise_x == current_x


def test_update_when_ship_hits_left_edge_no_movement_applied(ship_env):
    ship, *_ = ship_env
    left_edge = 0
    ship.precise_x = float(left_edge)
    ship.rect.x = left_edge
    ship.direction = ShipDirection.LEFT

    ship.update()

    assert ship.rect.x == left_edge


def test_update_when_ship_hits_right_edge_no_movement_applied(ship_env):
    ship, *_ = ship_env
    right_edge = ship.screen.get_rect().right
    ship.precise_x = float(right_edge)
    ship.rect.x = right_edge - ship.rect.width
    ship.direction = ShipDirection.RIGHT

    ship.update()

    assert ship.rect.x == right_edge