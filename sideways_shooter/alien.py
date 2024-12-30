import pygame
from pygame.sprite import Sprite

class Alien(pygame.sprite.Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ss_game, fleet_direction):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        self.fleet_direction = fleet_direction

        # Load the alien image and set its rect attribute.
        original_image = pygame.image.load('images/alien.png')

        # Scale by factor alien size.
        self.image = pygame.transform.scale(original_image,
         (int(original_image.get_width() * 0.75),
           int(original_image.get_height() * 0.75)))
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact vertical position.
        self.y = float(self.rect.y)

    def update(self):
        """Update the alien's position based on fleet direction."""
        self.rect.x += self.settings.alien_speed * self.fleet_direction
        
        # Move the alien vertically based on its fleet direction.
        self.rect.y += self.speed * self.fleet_direction

