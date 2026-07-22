import math


def test_update_when_less_than_max_speed_increases_speed(fake_game):
    difficulty = fake_game.difficulty
    difficulty.level = 4

    difficulty.update()

    assert math.isclose(difficulty.alien_speed, 1.4641)
    assert math.isclose(difficulty.bullet_speed, 3.20410338304)
    assert math.isclose(difficulty.ship_speed, 1.922462029824)


def test_update_when_at_max_speed_plateaus(fake_game):
    difficulty = fake_game.difficulty
    difficulty.level = 20

    difficulty.update()

    assert math.isclose(difficulty.alien_speed, 3.0)
    assert math.isclose(difficulty.bullet_speed, 5.0)
    assert math.isclose(difficulty.ship_speed, 3.5)