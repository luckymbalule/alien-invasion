"""Contain game difficulty and level up calculation and state"""


class Difficulty:
    """"""
    def __init__(self, settings):
        self.base_speed_scale = settings.base_speed_scale

        self.initial_alien_speed = settings.alien_speed
        self.max_alien_speed = settings.alien_speed_max
        self.alien_speed_scale = settings.alien_speed_scale

        self.initial_bullet_speed = settings.bullet_speed
        self.max_bullet_speed = settings.bullet_speed_max
        self.bullet_speed_scale = settings.bullet_speed_scale

        self.initial_ship_speed = settings.ship_speed
        self.max_ship_speed = settings.ship_speed_max
        self.ship_speed_scale = settings.ship_speed_scale

        self.reset()
        
    def update(self):
        self.level += 1

        self.alien_speed = self._get_speed(
            self.alien_speed_scale,
            self.initial_alien_speed,
            self.max_alien_speed
        )
        self.bullet_speed = self._get_speed(
            self.bullet_speed_scale,
            self.initial_bullet_speed,
            self.max_bullet_speed
        )
        self.ship_speed = self._get_speed(
            self.ship_speed_scale,
            self.initial_ship_speed,
            self.max_ship_speed
        )

    def reset(self):
        self.level = 0
        self.update()

    def _get_speed(self, scale, initial_speed, max_speed):
        growth_rate = (self.base_speed_scale - 1) * scale
        multiplier = 1 + growth_rate
        new_speed = initial_speed * (multiplier ** (self.level - 1))
        return min(new_speed, max_speed)