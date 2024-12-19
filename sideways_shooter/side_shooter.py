import pygame
import sys
from side_settings import Settings
from ss_ship import Jet
from side_bullet import Bullet
from alien import Alien

class SideShooter():
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((1200, 800))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Side Shooter')

        self.ship = Jet(self)

        # Create a group for bullets.
        self.bullets = pygame.sprite.Group()

        # Create a group of aliens.
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()  # Check for events like key presses.
            self.ship.update()  # Update position of the ship.
            self._update_bullets()  # Update the bullets.
            self._update_screen()  # Redraw the screen.
            self.clock.tick(60)  # Limit frame rate to 60 FPS.
    
    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()  # Create a bullet when space is pressed.   
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        
    def _check_keyup_events(self, event):
        """Respond to key release."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
    
    def _fire_bullet(self):
        """Create two bullets and add them to the bullet group."""
        # Adjust offset for left and right cannon.
        new_bullet_left = Bullet(self, offset_x=20, offset_y=15) # Left.
        new_bullet_right = Bullet(self, offset_x=20, offset_y=80) # Right.  

        self.bullets.add(new_bullet_left)  # Add it to the group
        self.bullets.add(new_bullet_right)
    
    def _update_bullets(self):
        """Update the position of bullets and remove off-screen ones."""
        self.bullets.update()  # Update all bullets in the group.

        # Remove bullets that are off the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.right < 0:
                self.bullets.remove(bullet)
    
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create the fleet of aliens.
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien height.
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        # Set the starting x position.
        # Near the right side, leaving space.
        start_x = (self.settings.screen_width - 2 * alien_width)
        current_x = start_x

        # Set the starting y position.
        current_y = alien_height
        while current_y < (self.settings.screen_height - 2 * alien_height):
            new_alien = Alien(self)
            new_alien.rect.x = current_x
            new_alien.rect.y = current_y
            self.aliens.add(new_alien)

            # Move down to the next row of aliens.
            current_y += alien_height
        
        # If you reach the bottom of the screen, start new column from right.
        if current_y > self.settings.screen_height:
            current_y = alien_height  # Reset y to the top
            current_x -= alien_width  # Move left for the next column.

    def _update_screen(self):
        """Update images on the screen, and flip to new screen."""
        self.screen.fill(self.settings.bg_color)
        # Draw the ship.
        self.ship.blitme()

        # Draw the bullets.
        self.bullets.draw(self.screen)

        # Draw the aliens.
        self.aliens.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game.
    ss = SideShooter()
    ss.run_game()

