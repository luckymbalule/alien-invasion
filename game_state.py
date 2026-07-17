"""
Centralise game phase, game state, and coordinate phase transitions and
publishing
"""


from enum import Enum


class GamePhase(Enum):
    PLAYING = "Playing"
    PAUSED = "Paused"
    GAME_OVER = "End"
    MENU = "Menu"


class GameState:
    """
    Store subscribers, ship count, mutate game phase and notify subscribers
    """

    def __init__(self, settings):
        self.settings = settings
        self.subscribers = []
        self.reset()

    def end(self):
        if self.phase == GamePhase.PLAYING:
            self._set_phase(GamePhase.GAME_OVER)

    def notify(self, phase):
        for subscriber in self.subscribers:
            subscriber(phase)

    def pause(self):
        if self.phase == GamePhase.PLAYING:
            self._set_phase(GamePhase.PAUSED)

    def register_ship_loss(self):
        if self.phase == GamePhase.PLAYING:
            self.ships_remaining -= 1
            if self.ships_remaining <= 0:
                self.end()

    def reset(self):
        """Reset phase and ships remaining to initial state"""
        self._set_phase(GamePhase.MENU)
        self.ships_remaining = self.settings.ship_limit

    def resume(self):
        if self.phase == GamePhase.PAUSED:
            self._set_phase(GamePhase.PLAYING)

    def start(self):
        if self.phase in (
            GamePhase.MENU, GamePhase.PAUSED, GamePhase.GAME_OVER
        ):
            self._set_phase(GamePhase.PLAYING)

    def subscribe(self, callback):
        if callback not in self.subscribers:
            self.subscribers.append(callback)

    def _set_phase(self, phase):
        """Set phase and notify subscribers"""
        self.phase = phase
        self.notify(self.phase)