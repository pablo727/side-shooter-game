import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ss_game, offset_x=0, offset_y=0):
        """Create a bullet object at the ship's current position,
        with optional offsets for left and right cannons.."""
        super().__init__()
        
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        self.color = self.settings.bullet_color
        self.image = pygame.image.load('images/bullet.png')

        # Create two bullets rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        
        # Set bullet position slightly ahead of the ship along the x and y.
        self.rect.x = ss_game.ship.rect.x + 92 + offset_x
        self.rect.y = ss_game.ship.rect.y + offset_y

        # Store the bullet position as float for smoother movement.
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet from left to right side."""
        # Update the exact position of the bullet.
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

        # Remove bullets if are off the screen.
        if self.rect.left > self.screen.get_rect().right:
            self.kill()

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)
