import pytest
from fleet import Fleet


@pytest.fixture
def fleet_env(fake_game):
    fleet = Fleet(fake_game.screen, fake_game.settings)
    yield fleet, fake_game.settings


def test_change_direction_when_fleet_hits_edge_drop_and_reverse_direction(
    fleet_env
):
    fleet, settings = fleet_env
    initial_y_position = [alien.rect.y for alien in fleet.aliens]
    initial_direction = fleet.direction

    fleet._change_direction()

    # Assert drop
    for initial_position, current_sprite in zip(
        initial_y_position, fleet.aliens
    ):
        assert current_sprite.rect.y == (
            initial_position + settings.fleet_drop_step
        )

    # Assert reverse direction
    assert fleet.direction != initial_direction

    # Assert strict boolean direction toggle behaviour
    fleet._change_direction()
    assert fleet.direction == initial_direction