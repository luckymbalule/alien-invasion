import pytest
import pygame
from settings import Settings
from difficulty import Difficulty
from fleet import Fleet
from ship import Ship
from game_state import GameState

class FakeGame:
    """Simplifies game environment for unit tests"""
    def __init__(self):
        self.settings = Settings()
        self.screen = pygame.Surface(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.game_state = GameState(self.settings)
        self.difficulty = Difficulty(self.settings)
        self.fleet = Fleet(self.screen, self.settings, self.difficulty)
        self.ship = Ship(self.screen, self.settings, self.difficulty)


@pytest.fixture
def fake_game():
    return FakeGame()


@pytest.fixture(autouse=True, scope="session")
def pygame_env():
    """
    Initialises a single headless SDL display for the testing session
    """
    pygame.init()
    pygame.display.set_mode((1,1), pygame.HIDDEN)

    yield
    
    pygame.quit()