import pytest
import pygame
from settings import Settings

class FakeGame:
    """Simplifies game environment for unit tests"""
    def __init__(self):
        self.settings = Settings()
        self.screen = pygame.Surface(
            (self.settings.screen_width, self.settings.screen_height)
        )


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