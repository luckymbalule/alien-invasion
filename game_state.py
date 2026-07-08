"""
Defines a centralised single source of truth for mutable game vairables
"""

class GameState:
    """Manages central state and lifecycle of the game"""

    def __init__(self, settings):
        self.settings = settings
        self.reset()

    def reset(self):
        """Resets mutable statistics and lifecycle flags"""
        self.is_active = True
        self.ships_remaining = self.settings.ship_limit