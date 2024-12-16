import pygame

class Jet():
    """A class to manage the jet."""

    def __init__(self, ss_game):
        """Initialize the ship and set its starting position."""
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        self.screen_rect = ss_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/jetfighter.png')

        # Change size of the ship as needed.
        self.image = pygame.transform.scale(self.image, (120, 120)) 

        self.rect = self.image.get_rect()

        # Set the initial position of the ship..
        self.rect.midleft = self.screen_rect.midleft

        # Flags for movement.
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the position of the ship based on movement flag."""
         # Prevent ship from moving off the top.
        if self.moving_up and self.rect.top > 0:  
            self.rect.y -= self.settings.ship_speed  # Move ship up.

        # Prevent ship from moving off the bottom.
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.settings.ship_speed  # Move ship down.

    def blitme(self):
        """Draw the jet at its current location."""
        self.screen.blit(self.image, self.rect)


