import pytest
import pygame
from settings import Settings

class MockGame:
    """A class to mimic game environment for unit tests"""
    def __init__(self):
        self.settings = Settings()
        self.screen = pygame.Surface(
            (self.settings.screen_width, self.settings.screen_height)
        )


@pytest.fixture(autouse=True, scope="session")
def mock_session():
    """
    Initialise a single headless SDL display for the entire test session
    """
    pygame.init()
    pygame.display.set_mode((1,1), pygame.HIDDEN)

    yield
    
    pygame.quit()


@pytest.fixture
def mock_game():
    return MockGame()