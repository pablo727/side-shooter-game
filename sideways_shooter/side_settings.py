class Settings:
    """A class to store all the settings for Side Shooter."""

    def __init__(self):
        """Initialize game's settings."""
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings.
        self.ship_speed = 5  # Set the ship speed.

        # Bullet settings.
        self.bullet_speed = 4
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
