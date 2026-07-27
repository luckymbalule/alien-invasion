"""Contain game difficulty and level up calculation and state"""


class Difficulty:
    """Manages difficulty progression and speed scaling across entities"""
    def __init__(self, settings):
        self.settings = settings
        self.base_speed_scale = self.settings.base_speed_scale

        self.initial_alien_speed = self.settings.alien_speed
        self.max_alien_speed = self.settings.alien_speed_max
        self.alien_speed_scale = self.settings.alien_speed_scale

        self.initial_bullet_speed = self.settings.bullet_speed
        self.max_bullet_speed = self.settings.bullet_speed_max
        self.bullet_speed_scale = self.settings.bullet_speed_scale

        self.initial_ship_speed = self.settings.ship_speed
        self.max_ship_speed = self.settings.ship_speed_max
        self.ship_speed_scale = self.settings.ship_speed_scale

        self.reset()
        
    def update(self):
        self.level += 1

        self.alien_speed = self._get_speed(
            self.alien_speed_scale,
            self.initial_alien_speed,
            self.max_alien_speed,
            True
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

    def _get_speed(self, scale, initial_speed, max_speed, lerp=False):
        """
        Calculate speed growth on current level, with an optional
        linear interpolation (lerp) for the final stretch to max speed

        Returns:
            New speed clamped between initial speed and max speed
        """
        speed = initial_speed
        growth_rate = (self.base_speed_scale - 1) * scale
        multiplier = 1 + growth_rate

        lerp_threshold = max_speed - self.settings.speed_lerp_range
        lerp_step_size = lerp_threshold / self.settings.speed_lerp_steps

        for _ in range(1, self.level):
            if lerp and speed >= lerp_threshold:
                speed += lerp_step_size
            else:
                speed *= multiplier

        return min(speed, max_speed)